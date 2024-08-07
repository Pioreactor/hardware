from pioreactor.background_jobs.od_reading import ADCReader
from pioreactor.actions.led_intensity import change_leds_intensities_temporarily
# this works with our ADS1115 board, probably with the Pico board...

adc = ADCReader(["1", "2"], fake_data=False, penalizer=0.0, dynamic_gain=False)
adc.tune_adc()

with change_leds_intensities_temporarily({'A': 50, 'B': 50, 'C': 50, 'D': 50}):

  while True:
      print(adc.take_reading())
