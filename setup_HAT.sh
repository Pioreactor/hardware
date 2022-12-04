#!/usr/bin/env bash

set -x
set -e

export LC_ALL=C

VERSION=1.0
UUID=$(python -c "import uuid;print(str(uuid.uuid4()))")
echo $UUID


(cd /home/pioreactor/hats/eepromutils && python3 write_eeprom.py $VERSION $UUID)

python3 HAT_tests.py

