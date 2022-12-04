### Write to EEPROM

Util to write to EEPROM our metadata.

Requires utils from the following project https://github.com/raspberrypi/hats.git

1. `git clone https://github.com/raspberrypi/hats.git && cd hats` to install eeprom utils if not already done.
2. Copy `write_eeprom.py` into the hats/eepromutils directory
3. Copy `pioreactor_eeprom_settings.txt.template` file into the hats/eepromutils directory

After set up is complete:

1. **Make sure the EEPROM pins are connected on the HAT using a jumper wire**.
2. `sudo python3 write_eeprom.py <version> <serial_number>`.
3. After a `sudo reboot`, try  `pio version -v` to confirm that HATs version.
