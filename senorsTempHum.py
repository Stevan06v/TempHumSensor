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

#define json obj
data = {
        "temperature": 0,
        "humidity": 0,
        "fullDate": "",
        "fullDate2": "",
        "fullDate3": "",
        "fullDate4": "",
        "date_time": ""
    }


def startupCheck():
    if os.path.isfile("data.json") and os.access("data.json", os.R_OK):
        # checks if file exists
        print("File exists and is readable")
    else:
        print("Either file is missing or is not readable, creating file...")
        # create json file
        with open("data.json", "w") as f:
            print("The json file is created.")


def calc_avgValue(values):
    sum = 0
    for iterator in values:
        sum += iterator
    return sum / len(values)


def onOFF():
    dataLED.on()
    time.sleep(0.7)
    dataLED.off()


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

            # init json object
            data["temperature"] = round(calc_avgValue(temp_values), 2)
            data["humidity"] = round(calc_avgValue(hum_values), 2)
            data["fullDate"] = today
            data["fullDate2"] = today.strftime("%d/%m/%Y")
            data["fullDate3"] = today.strftime("%B %d, %Y")
            data["fullDate4"] = today.strftime("%b-%d-%Y")
            data["date_time"] = now.strftime("%d/%m/%Y %H:%M:%S")


            #if data is written signal appears
            onOFF()
            print("Data has been written to data.json...")

            # Writing to sample.json
            with open("data.json", "w") as f:
                json.dump(data, f)

            counter = 0
    except RuntimeError as error:
        continue
    except Exception as error:
        
        sensor.exit()
        raise error
    time.sleep(0.2)

