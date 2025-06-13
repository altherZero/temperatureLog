import serial
import time
import openpyxl
from datetime import datetime

# === Configuration ===
PORT = 'COM7'       # Change this to your ESP32 port 
BAUDRATE = 115200
FILENAME = "temperature_log.xlsx"

# === Get User Input ===
try:
    sample_count = int(input("Numero de muestras: "))
    frequency = float(input("Frecuancia de muestreo  (e.g., 2.5): "))
except ValueError:
    print("Solo valores numericos.")
    exit()

# === Excel Workbook Setup ===
try:
    wb = openpyxl.load_workbook(FILENAME)
    ws = wb.active
except FileNotFoundError:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Timestamp"] + [f"Sensor {i+1}" for i in range(12)])

# === Initialize Serial ===
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Conectado A {PORT}, ESP32 reset...")
    time.sleep(2)
    ser.reset_input_buffer()
    print("listo")

    start = input("Press 'A' y Enter para iniciar: ").strip().upper()
    if start != 'A':
        print("Aborted by user.")
        ser.close()
        exit()

    print(f"iniciando: {sample_count} muestras cada {frequency} segundos.\n")

    for i in range(sample_count):
        ser.write(b'A')  # Send 'A' to ESP32
        time.sleep(0.1)

        line = ser.readline().decode('utf-8').strip()
        print(f"Sample {i+1}: {line}")

        try:
            values = [float(v) for v in line.split(',')]
            if len(values) == 12:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ws.append([timestamp] + values)
                wb.save(FILENAME)
            else:
                print(f"⚠️ Informacionincompleta. {len(values)}.")
        except ValueError:
            print("⚠️.Informacion erronea ")

        time.sleep(frequency)

    print("✅ Completo.")
except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")