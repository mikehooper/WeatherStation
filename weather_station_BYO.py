from gpiozero import Button
import time
import math
import bme280_sensor
import wind_direction_byo
import statistics
import ds18b20_therm
#import database

wind_count = 0    # Counts how many half-rotations
radius_cm = 9.0   # Radius of your anemometer
wind_interval = 5 # How often (secs) to sample speed
interval =  5     # measurements recorded every 5 minutes
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18
BUCKET_SIZE = 0.2794
rain_count = 0
gust = 0
store_speeds = []
store_directions = []

# Every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
    #print( wind_count )

def calculate_speed(time_sec):
    global wind_count
    global gust
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # Calculate distance travelled by a cup in km
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM

    # Speed = distance / time
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    # Calculate speed
    final_speed = km_per_hour * ADJUSTMENT

    return final_speed

def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    #print (rain_count * BUCKET_SIZE)

def reset_rainfall():
    global rain_count
    rain_count = 0

def reset_wind():
    global wind_count
    wind_count = 0

def reset_gust():
    global gust
    gust = 0

print('begin')

wind_speed_sensor = Button(5)
wind_speed_sensor.when_activated = spin
temp_probe = ds18b20_therm.DS18B20()

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

while True:
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        #time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction_byo.get_value())

        final_speed = calculate_speed(wind_interval)# Add this speed to the list
        store_speeds.append(final_speed)
        
    wind_average = wind_direction_byo.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()
    store_speeds = []
    #print(store_directions)
    store_directions = []
    ground_temp = temp_probe.read_temp()
    #ground_temp = 0
    humidity, pressure, ambient_temp = bme280_sensor.read_all()

    print('Wind Dir:',round(wind_average,1), 'Wind Speed:',round(wind_speed,1), 'Wind Gust:',round(wind_gust,1), 'Rainfall:',round(rainfall,1),'Humidity:',round(humidity,1),'Pressure:', round(pressure,1), 'Ambient Temp:',round(ambient_temp,1),'Ground Temp:', round(ground_temp,1))
    
    