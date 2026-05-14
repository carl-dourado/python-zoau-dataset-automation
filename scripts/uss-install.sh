#!/usr/bin/env sh
set -eu

chmod 755 member_copy.py copy_members.py
echo "Ready. Try: ./copy_members.py -i ZXP.PUBLIC.J2PDATA -o \"$USER.OUTPUT\" -m MEMBER1 -m MEMBER6"
