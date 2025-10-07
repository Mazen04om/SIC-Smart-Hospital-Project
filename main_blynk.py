#!/usr/bin/env python3
import time, ssl
from alarm import get_help
from bed_detection import beds_data
from dht import get_temp
from smoke import check_smoke
from paho.mqtt.client import Client, CallbackAPIVersion


# ========== Blynk Config ==========
BLYNK_TEMPLATE_NAME= "Smart hospital"
BLYNK_AUTH_TOKEN = "MnaFwbrHZDeTKnZmqHXr_AELrykhS79U"   
BLYNK_MQTT_BROKER = "blynk.cloud"

# ========== MQTT Setup ==========
mqtt = Client(CallbackAPIVersion.VERSION2)

def on_connect(mqtt, obj, flags, reason_code, properties):
    if reason_code == 0:
        print("[Connected to Blynk MQTT Broker")
    elif reason_code == "Bad user name or password":
        print("[Invalid BLYNK_AUTH_TOKEN")
        mqtt.disconnect()
    else:
        raise Exception(f"MQTT connection error: {reason_code}")

def on_message(mqtt, obj, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[↓] Downlink: {msg.topic} = {payload}")

mqtt.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.username_pw_set("device", BLYNK_AUTH_TOKEN)
mqtt.connect_async(BLYNK_MQTT_BROKER, 8883, 45)
mqtt.loop_start()

# ========== Main Loop ==========
while True:
    try:
        #reading the data of modules
        temp, hum = get_temp()
        bed1, bed2 = beds_data()
        alarm1, alarm2 = get_help()
        smoke_raw, smoke_alert = check_smoke()

        # print the values
        print("==== LIVE DATA ====")
        print(f" Temp: {temp} °C")
        print(f"Humidity: {hum} %")
        print(f"Bed1: {'Vacant' if bed1 else 'Occupied'}")
        print(f"Bed2: {'Vacant' if bed2 else 'Occupied'}")
        print(f"Alarm1: {alarm1}, Alarm2: {alarm2}")
        print(f" Smoke Raw: {smoke_raw}, Alert: {smoke_alert}")
        print("===================\n")

        # send the values to blink 
        mqtt.publish("ds/temp", str(int(temp)) if temp else "0")
        mqtt.publish("ds/hum", str(int(hum)) if hum else "0")
        mqtt.publish("ds/bed1", "1" if bed1 else "0")     # 1 = vacant
        mqtt.publish("ds/bed2", "1" if bed2 else "0")
        mqtt.publish("ds/alarm1", "1" if alarm1 else "0")
        mqtt.publish("ds/alarm2", "1" if alarm2 else "0")
        mqtt.publish("ds/smoke", "1" if smoke_alert else "0")
        mqtt.publish("ds/smoke_raw", str(smoke_raw) if smoke_raw else "0")

        # refreah every 3seconds
        time.sleep(3)

    except RuntimeError as e:
        print("[!] Sensor reading error:", e.args[0])
        time.sleep(2)
        continue
    except KeyboardInterrupt:
        print("\n Stopped by user.")
        break
    except Exception as e:
        raise e
