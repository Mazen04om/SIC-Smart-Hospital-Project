#!/usr/bin/env python3
import time
from alarm import get_help
from bed_detection import beds_data
from dht import get_temp
from smoke import check_smoke
import BlynkLib
from BlynkTimer import BlynkTimer

# ========== Blynk Config ==========
BLYNK_AUTH_TOKEN = "MnaFwbrHZDeTKnZmqHXr_AELrykhS79U"

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()

# ========== Connection Callback ==========
@blynk.on("connected")
def blynk_connected():
    print(" Connected to Blynk Cloud!")
    print(".......................................................")
    print("............. Smart Hospital Monitoring ...............")
    time.sleep(1)

# ========== Sensor Reading & Sending ==========
def send_data():
    try:
        # قراءة البيانات
        temp, hum = get_temp()
        bed1, bed2 = beds_data()
        alarm1, alarm2 = get_help()
        smoke_raw, smoke_alert = check_smoke()

        # طباعة القيم في التيرمينال
        print("==== LIVE DATA ====")
        print(f"Temp: {temp} °C")
        print(f"Humidity: {hum} %")
        print(f"Bed1: {'Vacant' if bed1 else 'Occupied'}")
        print(f"Bed2: {'Vacant' if bed2 else 'Occupied'}")
        print(f"Alarm1: {alarm1}, Alarm2: {alarm2}")
        print(f"Smoke Raw: {smoke_raw}, Alert: {smoke_alert}")
        print("===================\n")

        # إرسال القيم إلى Blynk
        # الحرارة والرطوبة والدخان → Integer
        blynk.virtual_write(0, int(temp) if temp else 0)          # V0
        blynk.virtual_write(1, int(hum) if hum else 0)            # V1
        blynk.virtual_write(7, int(smoke_raw) if smoke_raw else 0)# V2

        # حالة الأسرة → 1 vacant / 0 occupied
        blynk.virtual_write(2, 1 if bed1 else 0)                  # V3
        blynk.virtual_write(3, 1 if bed2 else 0)                  # V4

        # الطوارئ
        blynk.virtual_write(4, 1 if alarm1 else 0)                # V5
        blynk.virtual_write(5, 1 if alarm2 else 0)                # V6

        # تنبيه الدخان
        blynk.virtual_write(6, 1 if smoke_alert else 0)           # V7

    except RuntimeError as e:
        print("[!] Sensor reading error:", e.args[0])

# إرسال البيانات كل 3 ثواني
timer.set_interval(3, send_data)

# ========== Main Loop ==========
while True:
    blynk.run()
    timer.run()
