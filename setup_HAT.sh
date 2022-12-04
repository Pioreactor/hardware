#!/usr/bin/env bash

set -x
set -e

export LC_ALL=C

VERSION=1.0
UUID=$(python -c "import uuid;print(str(uuid.uuid4()))")
echo $UUID


python3 hats/eeprom_utils/write_eeprom.py $VERSION $UUID)

python3 tests/HAT_tests.py

