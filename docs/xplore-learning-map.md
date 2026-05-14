# IBM Z Xplore Learning Map

This project connects several Xplore topics into one small automation tool.

## JCL

The original workflow is an IEBCOPY job:

```jcl
//JOBSTEP EXEC PGM=IEBCOPY
//INDS    DD DISP=SHR,DSN=ZXP.PUBLIC.J2PDATA
//OUTDS   DD DISP=SHR,DSN=&SYSUID..OUTPUT
//SYSIN   DD *
  COPY OUTDD=OUTDS,INDD=INDS
  SELECT MEMBER=(MEMBER1,MEMBER6)
/*
```

In Python, the same idea becomes:

- build a DD list
- pass source and destination datasets as parameters
- generate the SYSIN control cards
- call `mvscmd.execute("IEBCOPY", dds=dd_list)`

## USS

The scripts are meant to live in the USS home directory and run with:

```sh
chmod 755 member_copy.py copy_members.py
./copy_members.py -i ZXP.PUBLIC.J2PDATA -o "$USER.OUTPUT" -m MEMBER1
```

## Datasets and PDS Members

The CLI validates dataset and member names before calling IEBCOPY. That catches
simple mistakes early while still letting the real z/OS utility report platform
specific errors.

## ZOAU

ZOAU provides the Python bridge into z/OS utility execution. The project keeps
ZOAU imports lazy so the repo can be tested on Linux while still running on USS.

## Error Handling

The SYSPRINT parser recognizes common IEBCOPY messages:

- missing member
- incompatible record format
- incompatible record length
- authorization failure
- missing input/output dataset surfaced through the return code and stderr

## Validation

IBM Z Xplore validates the challenge with:

```sh
submit "//'ZXP.PUBLIC.JCL(CHKJ2P1)'"
```

The validator expects `copy_members.py` to call `member_copy.py` and handle both
successful and failing inputs.
