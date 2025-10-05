from smoke import check_smoke
#from RPLCD.i2c import CharLCD
#from gpiozero import DigitalInputDevice
#from time import sleep
from bed_detection import beds_data
from dht import get_temp
import paho.mqtt.client as mqtt

mqttBroker = "f3d08ca9abd0489c86eb169ed4238783.s1.eu.hivemq.cloud"
port = 8883

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("Pi_Team5","RaspTeam5")
client.tls_set()

client.connect(mqttBroker,port)
client.loop_start()
"""
SENSOR1_PIN = 18
SENSOR2_PIN = 23
bed1 = DigitalInputDevice(SENSOR1_PIN, pull_up=True)
bed2 = DigitalInputDevice(SENSOR2_PIN, pull_up=True)

lcd = CharLCD('PCF8574', 0x27)
"""
print("IR Sensor (Active LOW) - Running...")

try:
    while True:
        smoke_alert, smoke_raw = check_smoke()
        temp, humi = get_temp()
        bed1, bed2 = beds_data()

        client.publish("Temp", temp)
        client.publish("Hum", humi)
        client.publish("Smoke", smoke_raw)
        client.publish("Bed_1", "Vacant" if bed1 else "Occupied")
        client.publish("Bed_2", "Vacant" if bed2 else "Occupied")

except KeyboardInterrupt:
    print("\n Stopped by user.")
