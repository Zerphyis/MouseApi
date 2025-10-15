import pyautogui

class MouseAction:
    def __init__(self):
        pyautogui.FAILSAFE = False

    def move(self, x, y):
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + x, current_y + y)
        print(f"Mouse movido para ({current_x + x}, {current_y + y})")

    def click(self, button="left"):
        pyautogui.click(button=button)
        print(f"Clique: {button}")

    def scroll(self, amount):
        pyautogui.scroll(amount)
        print(f"Scroll: {amount}")
