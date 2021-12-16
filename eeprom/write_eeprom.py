# util to write to EEPROM our metadata.
# this file should be placed in the raspberrypi/hats directory.
# run with sudo
import re
from datetime import datetime
import click
import subprocess


@click.command()
@click.argument('version')
def main(version):
    
    #1. create eeprom settings from template
    assert re.match(r"\d\.\d", version) is not None, "Version must be of the form x.y"
    major, minor = version.split(".")
    version_as_hex_string = "0x" + major.zfill(3) + minor
    current_time = datetime.utcnow().isoformat()

    with open("./pioreactor_eeprom_settings.txt.template", "r") as in_file:
        with open("./pioreactor_eeprom_settings.txt", "w") as out_file:
            eeprom_text = in_file.read().format(product_version=version_as_hex_string, current_time=current_time)
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


if __name__ == '__main__':
    main()