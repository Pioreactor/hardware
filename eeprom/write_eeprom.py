"""
util to write to EEPROM our metadata.

Requires utils from the following project https://github.com/raspberrypi/hats.git

0. `git clone https://github.com/raspberrypi/hats.git && cd hats`

1. Run `cd eepromutils && make && sudo make install` to install eeprom utils if not already done.

2. copy this Python file into the hats/eepromutils directory

3. copy eeprom_settings.txt.template file into the hats/eepromutils directory,

4. `sudo python3 write_eeprom.py 0.2`.

5. After a `sudo reboot`, try  `pio version -v` to confirm that HATs version.

TODO: it may fail the first time?? Try again.
"""
import re
from datetime import datetime
import click
import subprocess
import uuid


@click.command()
@click.argument('version')
def main(version):
    
    #1. create eeprom settings from template
    assert re.match(r"\d\.\d", version) is not None, "Version must be of the form x.y"
    major, minor = version.split(".")
    version_as_hex_string = "0x" + major.zfill(3) + minor
    current_time = datetime.utcnow().isoformat()
    serial_number = uuid.uuid4() # assign me externally / log me somewhere else
    product_name = "Pioreactor HAT"

    with open("./pioreactor_eeprom_settings.txt.template", "r") as in_file:
        with open("./pioreactor_eeprom_settings.txt", "w") as out_file:
            eeprom_text = in_file.read().format(product_version=version_as_hex_string, current_time=current_time, serial_number=serial_number, product_name=product_name)
            out_file.write(eeprom_text)
    
    # 2. compile to .eep file.
    output = subprocess.run(["./eepmake", "pioreactor_eeprom_settings.txt", "hat.eep"])
    if output.returncode != 0:
        print("Exiting due to error.")
        return

    # 3. write to hat
    output = subprocess.run(["./eepflash.sh", "-w" ,"-f=hat.eep" ,"-t=24c32", "-y"])
    if output.returncode != 0:
        print("Exiting due to error.")
        return

    return serial_number


if __name__ == '__main__':
    main()