class KeyboardAction:
    def __init__(self, controller):
        self.ctrl = controller


    def type_text(self, text, interval=0.0):
        self.ctrl.type_text(text, interval=float(interval))


    def press(self, key):
         self.ctrl.press_key(key)


    def hotkey(self, keys):
        self.ctrl.hotkey(*keys)