class MouseAction:
    def __init__(self, controller):
        self.ctrl = controller


    def move(self, dx, dy, absolute=False):
        self.ctrl.move_mouse(float(dx), float(dy), absolute=absolute)


    def click(self, button='left', clicks=1):
        self.ctrl.click(button=button, clicks=int(clicks))


    def scroll(self, amount):
        self.ctrl.scroll(int(amount))