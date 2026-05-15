from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import CopyRequest, ValidationError, build_tk5_iebcopy_jcl
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

    jcl_parser = subparsers.add_parser("jcl", help="print TK5/MVS IEBCOPY JCL")
    add_copy_arguments(jcl_parser)
    jcl_parser.add_argument("--job-name", default="CPYMEM", help="1-8 character TK5 job name")

    doctor_parser = subparsers.add_parser("doctor", help="check local TK5 demo and optional ZOAU bridge")
    doctor_parser.add_argument("--require-zoau", action="store_true", help="fail when zoautil_py is not importable")

    return parser


def add_copy_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-i", "--ifile", required=True, help="input PDS dataset name")
    parser.add_argument("-o", "--ofile", required=True, help="output PDS dataset name")
    parser.add_argument("-m", "--member", action="append", required=True, help="member to copy; can be repeated")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        print("TK5 demo mode is available: Python can generate IEBCOPY JCL and run the folder-backed PDS mock.")
        if ZoauDatasetRunner.is_available():
            print("Optional ZOAU bridge is available too.")
            return 0
        print("Optional ZOAU bridge is not available here; that is expected for the local TK5/Hercules demo.")
        return 1 if args.require_zoau else 0

    try:
        request = CopyRequest.from_values(args.ifile, args.ofile, args.member)
    except ValidationError as error:
        parser.error(str(error))

    if args.command == "plan":
        print(json.dumps(request.as_dict(), indent=2, sort_keys=True))
        return 0

    if args.command == "jcl":
        print(build_tk5_iebcopy_jcl(request, args.job_name), end="")
        return 0

    runner = MockDatasetRunner(Path(args.mock_root)) if args.mock_root else ZoauDatasetRunner()
    result = runner.copy_members(request)
    print(result.to_json() if args.json else result.message)
    return result.rc
