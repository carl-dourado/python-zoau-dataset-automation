from __future__ import annotations

from pathlib import Path


def read_syprint_lines(path: Path) -> list[str]:
    for encoding in ("cp1047", "cp037", "utf-8"):
        try:
            with path.open("r", encoding=encoding, errors="replace") as syprint:
                return syprint.readlines()
        except LookupError:
            continue
    with path.open("r", errors="replace") as syprint:
        return syprint.readlines()


def explain_iebcopy_error(syprint_path: str | Path, source: str, destination: str) -> str:
    path = Path(syprint_path)
    if not path.exists():
        return f"z/OS unchecked error. Expected SYSPRINT at {path}."

    message = ""
    bad_members: list[str] = []

    for line in read_syprint_lines(path):
        if "IGW01513T" in line:
            parts = line.split()
            if len(parts) > 11:
                message = (
                    "Record formats incompatible: "
                    f"{source} record format is {parts[7]} "
                    f"{destination} record format is {parts[11]}"
                )
        elif "IEB127I" in line:
            parts = line.split()
            if len(parts) > 7:
                input_recfm = parts[5][6:]
                output_recfm = parts[7][6:]
                message = (
                    "Record formats incompatible: "
                    f"{source} record format is {input_recfm} "
                    f"{destination} record format is {output_recfm}"
                )
        elif "IEB124I" in line:
            parts = line.split()
            if len(parts) > 9:
                input_lrecl = parts[5].strip("()")
                output_lrecl = parts[9].strip("().")
                message = (
                    "Record length incompatible: "
                    f"{source} record length is {input_lrecl} "
                    f"{destination} record length is {output_lrecl}"
                )
        elif "IEB177I" in line:
            parts = line.split()
            if len(parts) > 1:
                bad_members.append(parts[1])
        elif "913-00000038" in line:
            message = f"You are not authorized to {source}."

    if bad_members:
        if len(bad_members) == 1:
            return f"Member {bad_members[0]} is not in dataset {source}."
        return f"Members {', '.join(bad_members)} are not in dataset {source}."

    return message or f"z/OS unchecked error. Inspect {path}."
