#!/usr/bin/env bash

set -x
set -e

export LC_ALL=C

: ${1?"Usage: $0 HARDWARE_VERSION"}

HARDWARE_VERSION=$1
UUID=$(python -c "import uuid;print(str(uuid.uuid4()))")
echo $UUID
echo $HARDWARE_VERSION


(cd hats/eepromutils/; python3 write_eeprom.py $HARDWARE_VERSION $UUID)

HARDWARE=$HARDWARE_VERSION python3 tests/HAT_tests.py

