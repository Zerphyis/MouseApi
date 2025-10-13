import serial
import threading
import requests

class ArduinoController:
    def __init__(self, port="COM3", baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"[OK] Conectado à ESP32-C3 em {port}")
            self.connected_serial = True
        except:
            print("[!] Nenhum dispositivo serial encontrado. Tentando Wi-Fi...")
            self.connected_serial = False

        self.esp_ip = "192.168.4.1"  
        self.running = True

    def start_listening(self):
        if self.connected_serial:
            thread = threading.Thread(target=self.listen_serial, daemon=True)
            thread.start()

    def listen_serial(self):
        while self.running:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    print(f"[ESP32] {line}")

    def send_command(self, command):
        if self.connected_serial:
            self.ser.write((command + "\n").encode())
        else:
            try:
                r = requests.post(f"http://{self.esp_ip}/command", data=command, timeout=2)
                print(f"[Wi-Fi] {r.text}")
            except Exception as e:
                print(f"[ERRO Wi-Fi] {e}")
