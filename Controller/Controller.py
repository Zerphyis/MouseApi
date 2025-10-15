from Controller.MouseAction import MouseAction

class Controller:
    def __init__(self):
        self.mouse = MouseAction()
        self.arduino = None

    def set_arduino(self, arduino_controller):
        self.arduino = arduino_controller

    def move_mouse(self, request):
        data = request.get_json()
        x, y = data.get("x"), data.get("y")
        self.mouse.move(x, y)
        if self.arduino:
            self.arduino.send_command(f"MOUSE_MOVE:{x}:{y}")

    def click_mouse(self, request):
        data = request.get_json()
        button = data.get("button", "left")
        self.mouse.click(button)
        if self.arduino:
            self.arduino.send_command(f"MOUSE_CLICK:{button}")

    def scroll_mouse(self, request):
        data = request.get_json()
        amount = data.get("amount", 0)
        self.mouse.scroll(amount)
        if self.arduino:
            self.arduino.send_command(f"MOUSE_SCROLL:{amount}")

    def move_mouse_direct(self, x, y):
        self.mouse.move(x, y)

    def click_mouse_direct(self, button="left"):
        self.mouse.click(button)

    def scroll_mouse_direct(self, amount):
        self.mouse.scroll(amount)
