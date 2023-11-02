import click
from pioreactor.actions.self_test import test_positive_correlation_between_temperature_and_heating
from pioreactor.logging import create_logger
from pioreactor.hardware import is_heating_pcb_present, HALL_SENSOR_PIN
import lgpio
import time


def main():
    _handle = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_input(_handle, HALL_SENSOR_PIN, lgpio.SET_PULL_UP)

    lgpio.gpio_claim_alert(
        _handle, HALL_SENSOR_PIN, lgpio.FALLING_EDGE, lgpio.SET_PULL_UP
    )
    _edge_callback = lgpio.callback(
        _handle, HALL_SENSOR_PIN, lgpio.FALLING_EDGE
    )

    unit = "test"
    exp = "test"
    logger = create_logger("heating pcb test", unit=unit, experiment=exp, to_mqtt=False)

    click.echo("Is i2c 0x4F address filled?")
    assert is_heating_pcb_present()
    click.echo(" ✅")

    click.echo("Testing heating and temperature correlation")
    test_positive_correlation_between_temperature_and_heating(None, logger, unit, exp)
    click.echo(" ✅")

    click.echo("Hall sensor working?")
    click.echo("--> Wave both sides of a magnet in front of the Hall sensor")
    time.sleep(1)
    while _edge_callback.tally() == 0: # not sure if this works.
        print(f"saw {_edge_callback.tally()} pings")
        time.sleep(1)

    _edge_callback.cancel()
    click.echo(" ✅")
    click.echo("Completed ✅✅✅")


if __name__ == "__main__":
    main()
