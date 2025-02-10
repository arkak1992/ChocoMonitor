import serial
import time
import atexit
from threading import Thread, Event, Lock
import csv
import os
import datetime
import json

class ArduinoReader:
    def __init__(self, port='COM3', baudrate=115200, output_folder="data"):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False
        self.latest_temperature = None
        self.lock = Lock()
        self.stop_event = Event()
        self.output_folder = output_folder
        self.data_file = None
        self.settings = self.load_settings()  # تحميل الإعدادات
        atexit.register(self.cleanup)

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"start_temperature": 30, "duration": 5}

    def ensure_directory(self):
        today_folder = datetime.date.today().strftime("%Y-%m-%d")
        self.output_folder = os.path.join(self.output_folder, today_folder)
        os.makedirs(self.output_folder, exist_ok=True)
        self.data_file = os.path.join(
            self.output_folder,
            f"temperature_{datetime.datetime.now().strftime('%H-%M-%S')}.csv"
        )

    def connect(self):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                if self.ser and self.ser.is_open:
                    self.ser.close()
                self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
                time.sleep(2)
                self.ser.reset_input_buffer()
                print(f"✅ تم الاتصال بـ {self.port} بسرعة {self.baudrate}.")
                return True
            except serial.SerialException as e:
                print(f"❌ خطأ في الاتصال [{attempt+1}/5]: {e}")
                time.sleep(2)
        print("❌ فشل الاتصال بالأردوينو.")
        return False

    def start_reading(self):
        if not self.connect():
            return
        self.ensure_directory()
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self.read_loop, daemon=True)
        self.thread.start()

    def read_loop(self):
        with open(self.data_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["الوقت (ث)", "درجة الحرارة (°C)"])
            start_time = time.time()

            while self.running and not self.stop_event.is_set():
                try:
                    if self.ser and self.ser.in_waiting > 0:
                        data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                        if self.is_valid_temperature(data):
                            temp = round(float(data), 2)
                            elapsed_time = round(time.time() - start_time, 2)
                            writer.writerow([elapsed_time, temp])
                            csvfile.flush()

                            with self.lock:
                                self.latest_temperature = temp
                                print(f"🌡 التحديث: {temp} °C عند {elapsed_time} ثانية")
                except serial.SerialException:
                    print("🔌 فقدان الاتصال، جاري إعادة المحاولة...")
                    self.connect()
                except Exception as e:
                    print(f"⚠ خطأ غير متوقع: {e}")
                time.sleep(0.01)

    def is_valid_temperature(self, data):
        try:
            temp = float(data)
            return self.settings['start_temperature'] - 10 <= temp <= self.settings['start_temperature'] + 10
        except ValueError:
            return False

    def get_latest_temperature(self):
        with self.lock:
            return self.latest_temperature

    def stop_reading(self):
        self.running = False
        self.stop_event.set()
        self.cleanup()

    def cleanup(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 تم إغلاق الاتصال بالأردوينو.")

if __name__ == "__main__":
    reader = ArduinoReader()
    reader.start_reading()