import bme280
import smbus2
from time import sleep

port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def read_all():
    bme280_data = bme280.sample(bus,address)
    return bme280_data.humidity,bme280_data.pressure,bme280_data.temperature

#while True:
#    bme280_data = bme280.sample(bus,address)
#    humidity  = round(bme280_data.humidity,1)
#    pressure  = round(bme280_data.pressure,1)
#    ambient_temperature = round(bme280_data.temperature,1)
#    print('humidity',humidity, 'pressure',pressure, 'ambient_temperature',ambient_temperature)
#    sleep(1)