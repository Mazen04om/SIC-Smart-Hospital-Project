from RPLCD.i2c import CharLCD
from gpiozero import DigitalInputDevice
from time import sleep

SENSOR1_PIN = 18
SENSOR2_PIN = 23
bed1 = DigitalInputDevice(SENSOR1_PIN, pull_up=True)
bed2 = DigitalInputDevice(SENSOR2_PIN, pull_up=True)

lcd = CharLCD('PCF8574', 0x27)

def beds_data():
    try:
        state = []
        bed1_occ = not bed1.is_active
        state.append(1 if bed1_occ else 0)
        bed2_occ = not bed2.is_active
        state.append(1 if bed2_occ else 0)
        sleep(1)

        occupied = state.count(0)
        vacant = state.count(1)

        lcd.clear()
        lcd.write_string(f"Beds occupied: {occupied}")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Beds vacant: {vacant}")
        return bed1_occ, bed2_occ

    except KeyboardInterrupt:
        print("\n Stopped by user.")

    return None, None

