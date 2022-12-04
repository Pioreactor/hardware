#!/usr/bin/env bash

set -x
set -e

export LC_ALL=C

: ${1?"Usage: $0 HARDWARE_VERSION"}


UUID=$(python -c "import uuid;print(str(uuid.uuid4()))")
echo $UUID


python3 hats/eeprom_utils/write_eeprom.py $HARDWARE_VERSION $UUID)

python3 tests/HAT_tests.py

