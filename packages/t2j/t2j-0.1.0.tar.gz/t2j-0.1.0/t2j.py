"""t2j converts TOML input to JSON output and vice versa."""

import argparse
import collections.abc
import json
import sys
from contextlib import ExitStack

import tomli
import tomli_w

__version__ = '0.1.0'


def main():
    parser = argparse.ArgumentParser(
        description="Converts TOML to JSON (or JSON to TOML).")
    parser.add_argument('--toml-to-json', '-T', dest='direction',
                        action='store_const', const='t2j')
    parser.add_argument('--json-to-toml', '-J', dest='direction',
                        action='store_const', const='j2t')
    parser.add_argument('filename', nargs='?')
    parser.set_defaults(direction=parser.prog)
    args = parser.parse_args()
    with ExitStack() as close_stack:
        if args.filename is None:
            input_file = sys.stdin
        else:
            input_file = close_stack.enter_context(open(args.filename))
        output_file = sys.stdout
        if args.direction == 't2j':
            toml_object = tomli.load(input_file.buffer)
            json.dump(toml_object, output_file)
        elif args.direction == 'j2t':
            json_object = json.load(input_file)
            if not isinstance(json_object, collections.abc.Mapping):
                parser.error("input is not a JSON object")
            tomli_w.dump(json_object, output_file.buffer)
        else:
            parser.error(f"invalid conversion direction {args.direction!r}")
