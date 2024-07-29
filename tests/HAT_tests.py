from pioreactor.actions.led_intensity import led_intensity
import click
from time import sleep
from pioreactor.pubsub import publish
from pioreactor.hardware import *
from pioreactor import whoami
from pioreactor.utils.pwm import PWM
from pioreactor.actions.self_test import test_positive_correlation_between_temperature_and_heating
from pioreactor.logging import create_logger
from pioreactor.background_jobs.od_reading import ADCReader,ALL_PD_CHANNELS
import os

unit = whoami.get_unit_name()
experiment = whoami.UNIVERSAL_EXPERIMENT

def test_leds() -> bool:

    click.echo("Insert white LED into LED channels. Cycling through 0% to 50%.")
    click.echo("Ctrl-C to move on.")

    while True:
        try:
            for i in range(0, 50, 10):
                led_intensity({'A': i, 'B': i, 'C': i, 'D': i}, verbose=False)
                sleep(0.1)
            for i in range(50, 0, -10):
                led_intensity({'A': i, 'B': i, 'C': i, 'D': i}, verbose=False)
                sleep(0.1)
        except KeyboardInterrupt:
            led_intensity({'A': 0, 'B': 0, 'C': 0, 'D': 0})
            break

    return True


def test_correct_i2c_channels_on_HAT() -> bool:
    click.echo("Is i2c ADC and DAC address filled?")

    from busio import I2C  # type: ignore
    from adafruit_bus_device.i2c_device import I2CDevice  # type: ignore

    with I2C(SCL, SDA) as i2c:
        try:
            I2CDevice(i2c, DAC, probe=True)
            I2CDevice(i2c, ADC, probe=True)
            present = True
        except ValueError:
            present = False

    if present:
        click.echo("✅")
        return True
    else:
        click.echo("🛑")
        return False

def test_stemma_qt_is_available() -> bool:
    click.echo("Is stemma QT address filled (using AS7341 from adafruit)?")

    from busio import I2C  # type: ignore
    from adafruit_bus_device.i2c_device import I2CDevice  # type: ignore

    with I2C(SCL, SDA) as i2c:
        try:
            I2CDevice(i2c, 0x39, probe=True)
            present = True
        except ValueError:
            present = False

    if present:
        click.echo("✅")
        return True
    else:
        click.echo("🛑")
        return False


def test_shunt() -> bool:
    click.echo("Move shunt back and forth between pins. You should see 5V -> 12V -> 5V, ...")
    click.echo("Ctrl-C to move on.")

    while True:
        try:
            print(voltage_in_aux())
            sleep(0.5)
        except KeyboardInterrupt:
            break

    return True


def test_pwm() -> bool:

    click.echo("Setting all PWMs to 50%.")

    with PWM(PWM_TO_PIN["1"], 100, unit, experiment) as pwm1, \
         PWM(PWM_TO_PIN["2"], 100, unit, experiment) as pwm2, \
         PWM(PWM_TO_PIN["3"], 100, unit, experiment) as pwm3, \
         PWM(PWM_TO_PIN["4"], 100, unit, experiment) as pwm4:

        pwm1.start(50)
        pwm2.start(50)
        pwm3.start(50)
        pwm4.start(50)

        while True:
            try:
                sleep(0.5)
            except KeyboardInterrupt:
                break

    return True

def test_heating_pcb_connection() -> bool:
    click.echo("Testing heating PCB connection")

    # import test_hat, and run main()
    assert is_heating_pcb_present()
    while not click.confirm("Is heating PCB in HAT?"):
        pass

    logger = create_logger("test_heating_pcb_connection", unit=unit, experiment=experiment, to_mqtt=False)
    try:
        test_positive_correlation_between_temperature_and_heating(None, logger, unit, experiment)
        click.echo("✅")
        return True
    except:
        click.echo("🛑")
        return False


def test_eeprom_is_written(serial_number) -> bool:
    try:
        with open("/proc/device-tree/hat/uuid", "r") as f:
            text = f.read().rstrip("\x00")
            assert serial_number == text, "wrong serial_number provided"
            return True
    except:
        return False

def test_pds() -> bool:
    click.echo("Testing PDs. Move them around, wave your hand infront, etc. Look for responsiveness.")
    adc_reader = ADCReader(
        channels=ALL_PD_CHANNELS,
        dynamic_gain=False,
        fake_data=False,
        penalizer=0,
    )
    adc_reader.tune_adc()

    while True:
        try:
            print(adc_reader.take_reading())
            adc_reader.clear_batched_readings()
        except KeyboardInterrupt:
            break
    return True

def test_button() -> bool:
    click.confirm("Press the button... did the LED light up?")
    return True


@click.command()
def main() -> bool:

    click.confirm("""Setup:

 - EEPROM should have been written to.

 - Insert AS7341 from Adafruit into StemmaQT
 - Attach 12V PSU into barrel jack
 - Have a white LED nearby
 - Heating PCB is attached
 - PDs should be attached into channels 1 & 2
 - Stirring fan ready to test PWMs

Ready? """)

    # assert test_eeprom_is_written(serial_number), "EEPROM should have been written to."
    assert test_correct_i2c_channels_on_HAT()
    assert test_stemma_qt_is_available()

    # require manual testing
    assert test_leds()
    assert test_shunt()
    assert test_pwm()
    assert test_pds()
    assert test_button()
    assert test_heating_pcb_connection()


    click.echo("Test hat ✅")
    return True





if __name__ == "__main__":
    main()

