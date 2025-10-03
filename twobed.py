from RPLCD.i2c import CharLCD
from gpiozero import DigitalInputDevice
from time import sleep

SENSOR1_PIN = 18
SENSOR2_PIN = 23
bed1 = DigitalInputDevice(SENSOR1_PIN, pull_up=True)
bed2 = DigitalInputDevice(SENSOR2_PIN, pull_up=True)

lcd = CharLCD('PCF8574', 0x27)

print("IR Sensor (Active LOW) - Running...")

try:
    while True:
        state = []
        bed1_occ = not bed1.is_active
        state.append(1 if bed1_occ else 0)
        bed2_occ = not bed2.is_active
        state.append(1 if bed2_occ else 0)
        #print(f"Output = {output_value}")
        sleep(1)

        occupied = state.count(0)
        vacant = state.count(1)

        lcd.clear()
        lcd.write_string(f"Beds occupied: {occupied}")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Beds vacant: {vacant}")

except KeyboardInterrupt:
    print("\n Stopped by user.")
