# temperature_expansion_kit_test

from temperature_expansion_kit_plugin.max31865 import MAX31865
import board
import digitalio
import time

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
sensor = MAX31865(
    spi,
    cs,
    rtd_nominal=1000.0,
    ref_resistor=4300.0,
    wires=3,
    polarity=1,
)
while True:
    print(sensor.temperature)
    time.sleep(0.25)