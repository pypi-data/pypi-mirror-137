import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CLIArguments:
    path: Optional[Path]
    dump: bool
    keys: bool
    set: list[str]


def parse_arguments(
    dump_default: bool = False,
    keys_default: bool = False,
) -> CLIArguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=Path)
    parser.add_argument('--dump', default=dump_default, action='store_true')
    parser.add_argument('--keys', default=keys_default, action='store_true')
    parser.add_argument('--set', '-s', action='append', default=list())
    args = parser.parse_args()

    return CLIArguments(
        path=args.path,
        dump=args.dump,
        keys=args.keys,
        set=args.set,
    )
