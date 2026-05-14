from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DATASET_RE = re.compile(r"^[A-Z#$@][A-Z0-9#$@-]{0,7}(?:\.[A-Z#$@][A-Z0-9#$@-]{0,7})*$")
MEMBER_RE = re.compile(r"^[A-Z#$@][A-Z0-9#$@]{0,7}$")


class ValidationError(ValueError):
    """Raised when a dataset or member name is not valid for this workflow."""


@dataclass(frozen=True)
class CopyRequest:
    input_dataset: str
    output_dataset: str
    members: tuple[str, ...]

    @classmethod
    def from_values(cls, input_dataset: str, output_dataset: str, members: Iterable[str]) -> "CopyRequest":
        request = cls(
            input_dataset=normalize_dataset(input_dataset),
            output_dataset=normalize_dataset(output_dataset),
            members=tuple(normalize_member(member) for member in members),
        )
        request.validate()
        return request

    def validate(self) -> None:
        if not DATASET_RE.match(self.input_dataset):
            raise ValidationError(f"Invalid input dataset name: {self.input_dataset}")
        if not DATASET_RE.match(self.output_dataset):
            raise ValidationError(f"Invalid output dataset name: {self.output_dataset}")
        if not self.members:
            raise ValidationError("At least one member is required.")
        invalid_members = [member for member in self.members if not MEMBER_RE.match(member)]
        if invalid_members:
            raise ValidationError(f"Invalid member name(s): {', '.join(invalid_members)}")

    def as_dict(self) -> dict:
        return {
            "input_dataset": self.input_dataset,
            "output_dataset": self.output_dataset,
            "members": list(self.members),
            "control_cards": build_iebcopy_control_cards(self.members),
        }


@dataclass(frozen=True)
class CopyResult:
    rc: int
    message: str
    copied_members: tuple[str, ...] = ()
    syprint_path: str | None = None

    @property
    def ok(self) -> bool:
        return self.rc == 0

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "rc": self.rc,
            "message": self.message,
            "copied_members": list(self.copied_members),
            "syprint_path": self.syprint_path,
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2, sort_keys=True)


def normalize_dataset(value: str) -> str:
    return value.strip().upper()


def normalize_member(value: str) -> str:
    return value.strip().upper()


def build_iebcopy_control_cards(members: Iterable[str]) -> list[str]:
    member_string = ",".join(normalize_member(member) for member in members)
    return [
        " COPY OUTDD=OUTDS,INDD=INDS",
        f" SELECT MEMBER=({member_string})",
    ]


def dataset_to_mock_path(root: Path, dataset_name: str) -> Path:
    return root / normalize_dataset(dataset_name)
