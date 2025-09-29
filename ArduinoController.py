import serial
import threading
from Controller import Controller

class ArduinoController:
    def __init__(self, port="COM3", baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.controller = Controller()
        self.running = True

    def start_listening(self):
        thread = threading.Thread(target=self.listen_serial)
        thread.daemon = True
        thread.start()

    def listen_serial(self):
        while self.running:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    self.handle_command(line)

    def handle_command(self, command):
        parts = command.split(":")
        action = parts[0]

        if action == "MOUSE_MOVE" and len(parts) == 3:
            x, y = int(parts[1]), int(parts[2])
            self.controller.move_mouse_direct(x, y)

        elif action == "MOUSE_CLICK" and len(parts) == 2:
            button = parts[1]
            self.controller.click_mouse_direct(button)

        elif action == "MOUSE_SCROLL" and len(parts) == 2:
            amount = int(parts[1])
            self.controller.scroll_mouse_direct(amount)
