import serial
import time

PORT = 'COM7'      # Change this to match your port
BAUDRATE = 115200

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Wait for boot
    ser.reset_input_buffer()  # Clear any boot-up garbage
    print("Serial buffer cleared. Ready for commands.")
    print(f"Connected to {PORT}. Type 'A' and press Enter to request a float.")

    while True:
        user_input = input("Send command to ESP32: ").strip().upper()

        if user_input == 'A':
            ser.write(b'A')  # Send 'A' to ESP32
            print("Sent 'A'. Waiting for response...")

            response = ser.readline().decode('utf-8').strip()

            if response:
                try:
                    value = float(response)
                    print(f"Received float: {value}")
                except ValueError:
                    print(f"Received invalid data: {response}")
            else:
                print("No response received.")

        elif user_input == 'Q':
            print("Exiting.")
            break
        else:
            print("Only 'A' is valid to request data. Type 'Q' to quit.")

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")