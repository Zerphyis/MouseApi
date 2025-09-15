class MediaAction:
    def __init__(self, controller):
        self.ctrl = controller


    def play_pause(self):
        try:
              self.ctrl.press_key('playpause')
        except Exception:
                self.ctrl.press_key('space')


    def volume_up(self, steps=1):
        for _ in range(int(steps)):
            try:
                self.ctrl.press_key('volumeup')
            except Exception:
                self.ctrl.hotkey('ctrl', 'up')


    def volume_down(self, steps=1):
        for _ in range(int(steps)):
             try:
                self.ctrl.press_key('volumedown')
             except Exception:
                self.ctrl.hotkey('ctrl', 'down')

