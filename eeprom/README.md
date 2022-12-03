### Write to EEPROM

Util to write to EEPROM our metadata.

Requires utils from the following project https://github.com/raspberrypi/hats.git

0. `git clone https://github.com/raspberrypi/hats.git && cd hats`

1. Run `cd eepromutils && make && sudo make install` to install eeprom utils if not already done.

2. copy this Python file into the hats/eepromutils directory

3. copy eeprom_settings.txt.template file into the hats/eepromutils directory,

4. `sudo python3 write_eeprom.py 0.2 <serial_number>`.

5. After a `sudo reboot`, try  `pio version -v` to confirm that HATs version.

TODO: it may fail the first time?? Try again.