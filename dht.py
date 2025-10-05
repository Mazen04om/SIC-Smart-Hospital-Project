from time import sleep
import board
import adafruit_dht

sensor = adafruit_dht.DHT11(board.D4)

def get_temp():
    try:
        temp = sensor.temperature
        humi = sensor.humidity
        print(f"Temp={temp}ºC, Humidity={humi}%")
        return temp, humi

    except KeyboardInterrupt:
        print("\n Stopped by user.")

    except RuntimeError:
        return None, None

    sleep(1)
    return None

