import pyautogui
from interfaces.IAction import IAction

class KeyBoardAction(IAction):
    def type(self, text):
        pyautogui.write(text)

    def execute(self, *args, **kwargs):
        text = kwargs.get("text")
        if text:
            self.type(text)
