import serial
import threading
import requests
import socket

class ArduinoController:
    def __init__(self, port="COM3", baudrate=9600):
        self.ser = None
        self.connected_serial = False
        self.connected_wifi = False
        self.running = True
        self.esp_ip = None

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.connected_serial = True
            print(f"[OK] Conectado à ESP32-C3 via Serial ({port})")
        except Exception as e:
            print(f"[!] Serial não detectada ({e}). Tentando Wi-Fi...")
            self.connected_serial = False

        if not self.connected_serial:
            self.esp_ip = self._discover_esp_ip()
            if self.esp_ip:
                self.connected_wifi = True
                print(f"[OK] ESP32 detectada via Wi-Fi em {self.esp_ip}")
            else:
                print("[ERRO] Nenhum ESP32 encontrado na rede ou no modo AP.")

    def _discover_esp_ip(self):
        """
        Tenta descobrir o IP do ESP32-C3 na mesma rede
        usando o hostname padrão 'esp32-c3.local' ou fallback para 192.168.4.1.
        """
        try:
            ip = socket.gethostbyname("esp32-c3.local")
            return ip
        except Exception:
            return "192.168.4.1"

    def start_listening(self):
        if self.connected_serial:
            thread = threading.Thread(target=self.listen_serial, daemon=True)
            thread.start()
            print("[INFO] Escutando dados via Serial...")

    def listen_serial(self):
        while self.running:
            try:
                if self.ser and self.ser.in_waiting > 0:
                    line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                    if line:
                        print(f"[ESP32] {line}")
            except Exception as e:
                print(f"[ERRO Serial] {e}")
                break

    def send_command(self, command):
        """
        Envia um comando para o ESP32.
        O comando pode ser:
        - via Serial (USB)
        - via Wi-Fi (HTTP POST)
        """
        command = command.strip()
        if not command:
            print("[ERRO] Comando vazio.")
            return

        if self.connected_serial:
            try:
                self.ser.write((command + "\n").encode())
                print(f"[Serial → ESP32] {command}")
            except Exception as e:
                print(f"[ERRO Serial] {e}")

        elif self.connected_wifi:
            try:
                url = f"http://{self.esp_ip}/command"
                r = requests.post(url, data=command, timeout=3)
                print(f"[Wi-Fi → ESP32] {r.status_code} | {r.text}")
            except requests.exceptions.ConnectionError:
                print("[ERRO Wi-Fi] Conexão recusada. ESP32 pode estar desconectada.")
            except requests.exceptions.Timeout:
                print("[ERRO Wi-Fi] Tempo limite atingido.")
            except Exception as e:
                print(f"[ERRO Wi-Fi] {e}")
        else:
            print("[ERRO] Nenhum canal de comunicação ativo (Serial/Wi-Fi).")

    def stop(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[INFO] Conexão Serial encerrada.")
