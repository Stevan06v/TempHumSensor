import time
import board
import adafruit_dht
import psutil
import io
import json
import os
from gpiozero import LED
from datetime import date
from datetime import datetime

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == "libgpiod_pulsein" or proc.name() == "libgpiod_pulsei":
        proc.kill()
sensor = adafruit_dht.DHT11(board.D23)

# init
temp_values = [10]
hum_values = [10]
counter = 0
dataLED = LED(13)

def errSignal():
    for i in range(0,3):
        dataLED.on()
        time.sleep(0.1)
        dataLED.off()
        time.sleep(0.1)
        
#on startup
def runSignal():
    for i in range(0,5):
        dataLED.on()
        time.sleep(0.2)
        dataLED.off()
        time.sleep(0.2)

def startupCheck():
    if os.path.isfile("data.json") and os.access("data.json", os.R_OK):
        # checks if file exists
        print("File exists and is readable")
    else:
        print("Either file is missing or is not readable, creating file...")
        # create json file
        with open("data.json", "w") as f:
            print("The json file is created.")#
    
def calc_avgValue(values):
    sum = 0
    for iterator in values:
        sum += iterator
    return sum / len(values)


def onOFF():
    dataLED.on()
    time.sleep(0.7)
    dataLED.off()

# data led blinking on startup
runSignal()

# checks if file exists 
startupCheck()


while True:
    try:
        temp_values.insert(counter, sensor.temperature)
        hum_values.insert(counter, sensor.humidity)
        counter += 1
        time.sleep(6)
        if counter >= 10:
            print(
                "Temperature: {}*C   Humidity: {}% ".format(
                    round(calc_avgValue(temp_values), 2),
                    round(calc_avgValue(hum_values), 2),
                )
            )
            # get time
            today = date.today()
            now = datetime.now()

            
            # define json obj
            data = {
                "temperature": round(calc_avgValue(temp_values), 2),
                "humidity": round(calc_avgValue(hum_values), 2),
                "fullDate": str(today),
                "fullDate2": str(today.strftime("%d/%m/%Y")),
                "fullDate3": str(today.strftime("%B %d, %Y")),
                "fullDate4": str(today.strftime("%b-%d-%Y")),
                "date_time": str(now.strftime("%d/%m/%Y %H:%M:%S"))
            }

            # if data is written signal appears
            onOFF()
            
            print("Data has been written to data.json...")

            # Writing to sample.json
            with open("data.json", "w") as f:
                json.dump(data, f)

            counter = 0
    except RuntimeError as error:
        errSignal()
        continue
    except Exception as error:
        errSignal()
        sensor.exit()
        raise error
    time.sleep(0.2)

