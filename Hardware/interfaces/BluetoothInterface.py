import serial
import threading
import time

class BluetoothInterface:


    def __init__(self,port: str = "dev/rfcomm0",baudrate: int = 9600 , callback=None   ):
         self.port = port
         self.baudrate = baudrate
         self.serial_conn = None
         self.running = False
         self.callback = callback
         self.listener_thread = None 

    def connect(self, device_name: str = None) -> bool:

         try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            self.running = True
            self.listener_thread = threading.Thread(target=self._listen, daemon=True)
            self.listener_thread.start()
            print(f"[Bluetooth] Conectado em {self.port}")
            return True
         except Exception as e:
               print(f"[Bluetooth] Erro ao conectar: {e}")
               return False               
         
    def _listen(self):
        while self.running and self.serial_conn:
            try:
                line = self.serial_conn.readline().decode().strip()
                if line and self.callback:
                    import json
                    try:
                        event = json.loads(line)
                        self.callback(event)
                    except Exception:
                        print(f"[Bluetooth] Dados inválidos: {line}")
            except Exception as e:
                print(f"[Bluetooth] Erro leitura: {e}")
                time.sleep(1)     
 

    def send_event(self, event: dict) -> None:
        if self.serial_conn:
            data = (str(event) + "\n").encode()
            self.serial_conn.write(data)

    def disconnect(self) -> None:
        self.running = False
        if self.serial_conn:
            self.serial_conn.close()
            self.serial_conn = None
        print("[Bluetooth] Desconectado")