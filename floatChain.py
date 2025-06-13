import serial
import time

PORT = 'COM7'      # or '/dev/ttyUSB0'
BAUDRATE = 115200

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Connected to {PORT}. Waiting for ESP32 reset...")
    time.sleep(2)
    ser.reset_input_buffer()
    print("Ready.")

    while True:
        cmd = input("Press A to get 12 float values (Q to quit): ").strip().upper()
        
        if cmd == 'A':
            ser.write(b'A')
            time.sleep(0.1)  # Allow ESP32 to respond

            line = ser.readline().decode('utf-8').strip()
            print("Raw response:", line)

            try:
                values = [float(v) for v in line.split(',')]
                if len(values) == 12:
                    print("Received 12 floats:", values)
                else:
                    print(f"Expected 12 values, got {len(values)}")
            except ValueError:
                print("Invalid float values received.")

        elif cmd == 'Q':
            break
        else:
            print("Only 'A' is valid to get data. Use 'Q' to quit.")

except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")