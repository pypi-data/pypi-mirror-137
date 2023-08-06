#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entry-point into the 'xlf_merge' application.

This is a XLF Merge

License: GPL
Website: https://github.com/Salamek/xlf-merge

Command details:
    merge              Merge XLF files
    dupes              Find dupes in file

Usage:
    xlf-merge merge <from_file> <with_file> <output_file> [-m METHOD]
    xlf-merge dupes <file> [-m METHOD]
    xlf-merge (-h | --help)

Options:

    -m METHOD --method=METHOD        Type of merge used, source, id, or target when finding dupes
                                     [default: source]

"""

import sys
import signal
from typing import List
from functools import wraps
from xlf_merge.XlfParser import XlfParser

from docopt import docopt

OPTIONS = docopt(__doc__)


def find_trans_unit(needle: str, trans_units: List[dict], key: str) -> List[dict]:
    if key.startswith('@'):
        return list(filter(lambda d: d[1]['attrib'][key] == needle, enumerate(trans_units)))
    return list(filter(lambda d: d[1][key] == needle, enumerate(trans_units)))


def command(func):
    """Decorator that registers the chosen command/function.

    If a function is decorated with @command but that function name is not a valid "command" according to the docstring,
    a KeyError will be raised, since that's a bug in this script.

    If a user doesn't specify a valid command in their command line arguments, the above docopt(__doc__) line will print
    a short summary and call sys.exit() and stop up there.

    If a user specifies a valid command, but for some reason the developer did not register it, an AttributeError will
    raise, since it is a bug in this script.

    Finally, if a user specifies a valid command and it is registered with @command below, then that command is "chosen"
    by this decorator function, and set as the attribute `chosen`. It is then executed below in
    `if __name__ == '__main__':`.

    Doing this instead of using Flask-Script.

    Positional arguments:
    func -- the function to decorate
    """
    @wraps(func)
    def wrapped():
        return func()

    # Register chosen function.
    if func.__name__ not in OPTIONS:
        raise KeyError('Cannot register {}, not mentioned in docstring/docopt.'.format(func.__name__))
    if OPTIONS[func.__name__]:
        command.chosen = func

    return wrapped


@command
def merge() -> None:

    with open(OPTIONS['<from_file>'], 'r') as from_file_handle:
        from_file = from_file_handle.read()

    with open(OPTIONS['<with_file>'], 'r') as with_file_handle:
        with_file = with_file_handle.read()

    from_file_xlf_parser = XlfParser.from_xml(from_file)
    with_file_xlf_parser = XlfParser.from_xml(with_file)

    from_file_trans_units = from_file_xlf_parser.get_trans_units()
    with_file_trans_units = with_file_xlf_parser.get_trans_units()

    key = {
        'id': '@id',
        'source': 'source'
    }.get(OPTIONS['--method'])

    if not key:
        raise Exception('Unknown match method {}'.format(OPTIONS['--method']))

    # We are merging from_file to with_file
    # That means list over stuff in from_file and merge it into with_file

    for from_file_trans_unit in from_file_trans_units:
        if not from_file_trans_unit.get('target'):
            continue
        for (found_index, found_trans_unit) in find_trans_unit(from_file_trans_unit[key], with_file_trans_units, key):
            # Modify found trans_unit with new info
            found_trans_unit['target'] = from_file_trans_unit['target']

            # Delete old item,
            del with_file_trans_units[found_index]
            with_file_trans_units.insert(found_index, found_trans_unit)

    final_xlf_parser = XlfParser.from_trans_units(with_file_trans_units)
    pretty_print_output = final_xlf_parser.to_xml()

    with open(OPTIONS['<output_file>'], 'w') as output_file_handle:
        output_file_handle.write(pretty_print_output)


@command
def dupes():
    with open(OPTIONS['<file>'], 'r') as file_handle:
        file = file_handle.read()

    from_file_xlf_parser = XlfParser.from_xml(file)
    file_trans_units = from_file_xlf_parser.get_trans_units()

    key = {
        'id': '@id',
        'source': 'source',
        'target': 'target'
    }.get(OPTIONS['--method'])

    if not key:
        raise Exception('Unknown match method {}'.format(OPTIONS['--method']))

    matches = {}  # key to int
    for file_trans_unit in file_trans_units:
        if not isinstance(file_trans_unit[key], str):
            continue
        if file_trans_unit[key] in matches:
            matches[file_trans_unit[key]] += 1
        else:
            matches[file_trans_unit[key]] = 1

    for mkey, value in matches.items():
        if value > 1:
            print('{}="{}" was found {} times!'.format(key, mkey, value))

    print('Done!')


def main() -> None:
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))  # Properly handle Control+C
    getattr(command, 'chosen')()  # Execute the function specified by the user.


if __name__ == '__main__':
    main()

