### HAT hardware setup

#### Installation

1. git clone this repo to your Raspberry Pi: `git clone https://github.com/Pioreactor/hardware.git && cd hardware`
2. Install eeprom utils: `cd hats/eepromutils && make && sudo make install`
3. Move some files over: `mv ../eeprom/write_eeprom.py . && mv ../eeprom/pioreactor_eeprom_settings.txt.template .`


#### Setting up a new HAT

0. Attach the HAT to the RPi.
1. Run `sudo bash setup_HAT.py`
2. Record the serial number/UUID
2. After a `sudo reboot`, try  `pio version -v` to confirm that HATs version.
