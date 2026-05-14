from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import CopyRequest, ValidationError
from .mock_runner import MockDatasetRunner
from .zoau_runner import ZoauDatasetRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mainframe-dataset")
    subparsers = parser.add_subparsers(dest="command", required=True)

    copy_parser = subparsers.add_parser("copy", help="copy members between PDS datasets")
    add_copy_arguments(copy_parser)
    copy_parser.add_argument("--mock-root", help="use local folder-backed datasets instead of ZOAU")
    copy_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    plan_parser = subparsers.add_parser("plan", help="print the IEBCOPY plan without executing")
    add_copy_arguments(plan_parser)

    subparsers.add_parser("doctor", help="check whether ZOAU is importable")

    return parser


def add_copy_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-i", "--ifile", required=True, help="input PDS dataset name")
    parser.add_argument("-o", "--ofile", required=True, help="output PDS dataset name")
    parser.add_argument("-m", "--member", action="append", required=True, help="member to copy; can be repeated")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        if ZoauDatasetRunner.is_available():
            print("ZOAU imports are available.")
            return 0
        print("ZOAU imports are not available here. Use --mock-root locally or run this on z/OS USS.")
        return 1

    try:
        request = CopyRequest.from_values(args.ifile, args.ofile, args.member)
    except ValidationError as error:
        parser.error(str(error))

    if args.command == "plan":
        print(json.dumps(request.as_dict(), indent=2, sort_keys=True))
        return 0

    runner = MockDatasetRunner(Path(args.mock_root)) if args.mock_root else ZoauDatasetRunner()
    result = runner.copy_members(request)
    print(result.to_json() if args.json else result.message)
    return result.rc
