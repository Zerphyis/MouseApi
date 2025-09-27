import pyautogui
from interfaces.IAction import IAction

class MouseAction(IAction):
    def move(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self, button="left"):
        pyautogui.click(button=button)

    def execute(self, *args, **kwargs):
        action = kwargs.get("action")
        if action == "move":
            self.move(kwargs["x"], kwargs["y"])
        elif action == "click":
            self.click(kwargs.get("button", "left"))
