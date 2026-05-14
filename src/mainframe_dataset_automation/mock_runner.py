from __future__ import annotations

import shutil
from pathlib import Path

from .core import CopyRequest, CopyResult, dataset_to_mock_path


class MockDatasetRunner:
    """Local folder-based runner for demos and tests.

    A dataset is represented by a directory and each member is represented by a
    file inside that directory.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def copy_members(self, request: CopyRequest) -> CopyResult:
        source = dataset_to_mock_path(self.root, request.input_dataset)
        destination = dataset_to_mock_path(self.root, request.output_dataset)

        if not source.exists():
            return CopyResult(8, f"Error connecting to {request.input_dataset} - It probably doesn't exist.")

        destination.mkdir(parents=True, exist_ok=True)
        copied: list[str] = []
        missing: list[str] = []

        for member in request.members:
            source_member = source / member
            if not source_member.exists():
                missing.append(member)
                continue
            shutil.copyfile(source_member, destination / member)
            copied.append(member)

        if missing:
            if len(missing) == 1:
                return CopyResult(12, f"Member {missing[0]} is not in dataset {request.input_dataset}.", tuple(copied))
            return CopyResult(12, f"Members {', '.join(missing)} are not in dataset {request.input_dataset}.", tuple(copied))

        return CopyResult(0, "Members copied!", tuple(copied))
