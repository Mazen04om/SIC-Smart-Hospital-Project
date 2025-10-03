from gpiozero import DigitalInputDevice
from time import sleep

SENSOR_PIN = 18
ir_sensor = DigitalInputDevice(SENSOR_PIN, pull_up=True)

print("IR Sensor (Active LOW) - Running...")

try:
    while True:
        person_detected = not ir_sensor.is_active
        output_value = 1 if person_detected else 0
        print(f"Output = {output_value}")
        sleep(5)

except KeyboardInterrupt:
    print("\n Stopped by user.")
