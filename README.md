### HAT hardware setup

#### Installation

1. git clone this repo to your Raspberry Pi: `git clone --recurse-submodules https://github.com/Pioreactor/hardware.git && cd hardware`
2. Install eeprom utils: `cd hats/eepromutils && make && sudo make install && cd ..`

# I think this is wrong below?
4. Move some files over: `mv ../eeprom/write_eeprom.py eepromutils/ && mv ../eeprom/pioreactor_eeprom_settings.txt.template eepromutils/`


#### Setting up a new HAT

0. Attach the HAT to the RPi.
1. Run `sudo bash setup_HAT.py`
2. Record the serial number/UUID
2. After a `sudo reboot`, try  `pio version -v` to confirm that HATs version.
