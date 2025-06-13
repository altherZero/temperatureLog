import serial
import time
import openpyxl
from datetime import datetime

PORT = 'COM7'       # Replace with your serial port
BAUDRATE = 115200
FILENAME = "temperature_log.xlsx"

# Initialize Excel workbook
try:
    wb = openpyxl.load_workbook(FILENAME)
    ws = wb.active
except FileNotFoundError:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Timestamp"] + [f"Sensor {i+1}" for i in range(12)])

# Initialize serial connection
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Connected to {PORT}. Waiting for ESP32 reset...")
    time.sleep(2)
    ser.reset_input_buffer()
    print("Ready to receive values.")

    while True:
        cmd = input("Press A to get 12 float values (Q to quit): ").strip().upper()

        if cmd == 'A':
            ser.write(b'A')
            time.sleep(0.1)

            line = ser.readline().decode('utf-8').strip()
            print("Raw response:", line)

            try:
                values = [float(v) for v in line.split(',')]
                if len(values) == 12:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ws.append([timestamp] + values)
                    wb.save(FILENAME)
                    print(f"Logged at {timestamp}: {values}")
                else:
                    print(f"Expected 12 values, got {len(values)}")
            except ValueError:
                print("Invalid float values received.")

        elif cmd == 'Q':
            print("Exiting.")
            break
        else:
            print("Only 'A' is valid to get data. Use 'Q' to quit.")

except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")