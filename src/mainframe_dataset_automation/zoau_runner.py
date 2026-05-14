from __future__ import annotations

import os
from pathlib import Path

from .core import CopyRequest, CopyResult, build_iebcopy_control_cards
from .errors import explain_iebcopy_error


class ZoauDatasetRunner:
    """Runner that calls IEBCOPY through ZOAU.

    Imports are intentionally lazy so the package can be tested on machines that
    do not have ZOAU installed.
    """

    def __init__(self, syprint_path: str | Path | None = None) -> None:
        self.syprint_path = Path(syprint_path or Path.home() / "copy_output")

    @staticmethod
    def is_available() -> bool:
        try:
            import mvs_command_support  # noqa: F401
            import zoautil_py  # noqa: F401
        except ImportError:
            return False
        return True

    def copy_members(self, request: CopyRequest) -> CopyResult:
        from mvs_command_support import cleanup_temporaries, create_input_dd
        from zoautil_py import mvscmd
        from zoautil_py.types import DDStatement, DatasetDefinition, FileDefinition

        dd_list = [
            DDStatement("INDS", DatasetDefinition(request.input_dataset)),
            DDStatement("OUTDS", DatasetDefinition(request.output_dataset)),
            DDStatement("SYSPRINT", FileDefinition(str(self.syprint_path))),
            create_input_dd(build_iebcopy_control_cards(request.members), ddname="SYSIN"),
        ]

        response = mvscmd.execute("IEBCOPY", dds=dd_list)
        result = response.to_dict()
        return_code = int(result["rc"])
        stderr_response = result.get("stderr_response", "")

        try:
            if return_code == 0:
                if self.syprint_path.exists():
                    os.remove(self.syprint_path)
                return CopyResult(0, "Members copied!", request.members)

            if return_code == 8:
                if "INDS" in stderr_response:
                    message = f"Error connecting to {request.input_dataset} - It probably doesn't exist."
                else:
                    message = f"Error connecting to {request.output_dataset} - It probably doesn't exist."
                return CopyResult(return_code, message, syprint_path=str(self.syprint_path))

            message = explain_iebcopy_error(self.syprint_path, request.input_dataset, request.output_dataset)
            return CopyResult(return_code, message, syprint_path=str(self.syprint_path))
        finally:
            cleanup_temporaries()
