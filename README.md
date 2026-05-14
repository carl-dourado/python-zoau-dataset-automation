# Python ZOAU Dataset Automation

Converts a small IBM Z utility workflow from JCL/IEBCOPY into Python that can be
called from USS, tested locally, and validated by the IBM Z Xplore `CHKJ2P1` job.

The project is based on IBM Z Xplore labs around JCL, USS, datasets, PDS members,
and the J2P1 "JCL to Python" challenge. IBM course PDFs are not redistributed
here; this repo contains my implementation, notes, and reproducible local tests.

## What It Proves

- Python running in USS
- ZOAU `mvscmd.execute()` integration
- JCL DD concepts translated into Python objects
- IEBCOPY member copy from one PDS to another
- CLI argument parsing for input dataset, output dataset, and member list
- Error handling for missing datasets, bad members, and incompatible datasets
- Local mock mode so the behavior can be reviewed without a mainframe login

## Repository Layout

```text
.
├── src/mainframe_dataset_automation/  # reusable package and CLI
├── member_copy.py                     # IBM Z Xplore validator-compatible module
├── copy_members.py                    # IBM Z Xplore validator-compatible CLI
├── examples/mock_zos/                 # local PDS-like mock folders
├── tests/                             # stdlib unittest suite
└── docs/xplore-learning-map.md        # study notes mapped to project features
```

## Run Locally Without z/OS

The local mode treats folders as PDS datasets and files as members.

```sh
python -m unittest discover -s tests

PYTHONPATH=src python -m mainframe_dataset_automation \
  copy \
  --mock-root examples/mock_zos \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6 \
  --json
```

After running mock mode, copied members appear under:

```text
examples/mock_zos/Z49216.OUTPUT/
```

## Run On IBM Z Xplore USS

Copy these two root-level files to your USS home directory:

- `member_copy.py`
- `copy_members.py`

Then run:

```sh
chmod 755 member_copy.py copy_members.py
./copy_members.py -i ZXP.PUBLIC.J2PDATA -o "$USER.OUTPUT" -m MEMBER1 -m MEMBER6
submit "//'ZXP.PUBLIC.JCL(CHKJ2P1)'"
```

`CHKJ2P1` expects `copy_members.py` in the USS home directory and validates that it
uses `member_copy.py` to handle both successful and failing copy scenarios.

## CLI Examples

Plan the copy without executing it:

```sh
PYTHONPATH=src python -m mainframe_dataset_automation plan \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6
```

Check whether the current environment can import ZOAU:

```sh
PYTHONPATH=src python -m mainframe_dataset_automation doctor
```

Use the package CLI on z/OS:

```sh
PYTHONPATH=src python -m mainframe_dataset_automation copy \
  -i ZXP.PUBLIC.J2PDATA \
  -o "$USER.OUTPUT" \
  -m MEMBER1 \
  -m MEMBER3 \
  -m MEMBER6
```

## Notes

The root-level `member_copy.py` and `copy_members.py` are intentionally small and
self-contained because the Xplore validator looks for those exact files in the USS
home directory. The package under `src/` is the cleaner, testable version for the
portfolio and future extension.
