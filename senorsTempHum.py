import time
import board
import adafruit_dht
import psutil

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D23)

temp_values = [10]
hum_values = [10]
counter = 0
def calc_avgValue(values):
    sum = 0
    for iterator in values:
        sum += iterator
    return sum/len(values)

while True:
    try:
        temp_values.insert(counter, sensor.temperature)
        hum_values.insert(counter, sensor.humidity)
        counter += 1
        time.sleep(6)
        if counter >= 10:
            print("Temperature: {}*C   Humidity: {}% ".format(round(calc_avgValue(temp_values), 2), round(calc_avgValue(hum_values), 2)))
            counter = 0
    except RuntimeError as error:
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(0.2)