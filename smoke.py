import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def check_smoke():
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            raw = int(line)
            print("Received:", raw)
            if (raw > 180):
                danger = 1
            else:
                danger = 0
            return raw, danger

        except KeyboardInterrupt:
            print("\n Stopped by user.")

    return None, None
