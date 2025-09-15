import io

try:
    import pyautogui
except Exception:
    pyautogui = None

from .config import Config


class InputController:
    def __init__(self):
        self.available = pyautogui is not None
        if not self.available:
            print('[WARN] pyautogui não disponível')
        else:
            pyautogui.FAILSAFE = False

    def move_mouse(self, dx, dy, absolute=False):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        if absolute:
            pyautogui.moveTo(int(dx), int(dy))
        else:
            pyautogui.moveRel(
                int(dx * Config.MOUSE_SENSITIVITY),
                int(dy * Config.MOUSE_SENSITIVITY)
            )

    def click(self, button='left', clicks=1, interval=0.0):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        pyautogui.click(button=button, clicks=clicks, interval=interval)

    def scroll(self, amount):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        pyautogui.scroll(int(amount))

    def type_text(self, text, interval=0.0):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        pyautogui.typewrite(text, interval=interval)

    def press_key(self, key):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        pyautogui.press(key)

    def hotkey(self, *keys):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        pyautogui.hotkey(*keys)

    def screenshot(self, region=None):
        if not self.available:
            raise RuntimeError('pyautogui não disponível')
        img = pyautogui.screenshot(region=region)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf.read()
