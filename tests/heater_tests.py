import click
from pioreactor.actions.self_test import test_positive_correlation_between_temperature_and_heating
from pioreactor.logging import create_logger
from pioreactor.hardware import is_heating_pcb_present, HALL_SENSOR_PIN
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def main():

    unit = "test"
    exp = "test"
    logger = create_logger("heating pcb test", unit=unit, experiment=exp, to_mqtt=False)

    click.echo("Is i2c 0x4F address filled?")
    is_heating_pcb_present()
    click.echo(" ✅")

    click.echo("Testing heating and temperature correlation")
    test_positive_correlation_between_temperature_and_heating(None, logger, unit, exp)
    click.echo(" ✅")

    click.echo("Hall sensor working?")
    click.echo("--> Wave both sides of a magnet in front of the Hall sensor")

    GPIO.setup(HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.wait_for_edge(HALL_SENSOR_PIN, GPIO.RISING)
    click.echo(" ✅")
    click.echo("Completed ✅✅✅")


if __name__ == "__main__":
    main()