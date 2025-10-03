import serial
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)

ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            lcd.clear()
            raw = int(line)
            print("Received:", raw)
            if (raw > 180):
                lcd.write_string("Smoke Detected")
            else:
                lcd.write_string("All Good")

except KeyboardInterrupt:
    print("\n Stopped by user.")
