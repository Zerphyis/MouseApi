import pyautogui

class MouseAction:
    def move(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self, button="left"):
        pyautogui.click(button=button)

    def scroll(self, amount):
        pyautogui.scroll(amount)
