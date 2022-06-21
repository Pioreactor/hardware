# util to write to EEPROM our metadata.
#
# Requires utils from the following project:
# > git clone https://github.com/raspberrypi/hats.git
#
# 1. Run `cd eepromutils && make && sudo make install` to install eeprom utils if not already done.
#
# 2. this Python file should be placed in the raspberrypi/hats/eepromutils directory,
# 
# 3. Place eeprom_settings.txt.template file in raspberrypi/hats/eepromutils directory
# run with sudo, ex:
#
# > sudo python3 write_eeprom.py 0.2
#
# TODO: it may fail the first time?? Try again.
# 
# 4. Reboot
#
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
    serial_number = uuid.uuid4() # log me somewhere else

    with open("./pioreactor_eeprom_settings.txt.template", "r") as in_file:
        with open("./pioreactor_eeprom_settings.txt", "w") as out_file:
            eeprom_text = in_file.read().format(product_version=version_as_hex_string, current_time=current_time, serial_number=serial_number)
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
