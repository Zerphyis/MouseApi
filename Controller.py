from actions.MouseAction import MouseAction
from actions.KeyBoardAction import KeyBoardAction
from actions.MediaAction import MediaAction
from actions.FileManager import FileManager

class Controller:
    def __init__(self):
        self.mouse = MouseAction()
        self.keyboard = KeyBoardAction()
        self.media = MediaAction()
        self.file_manager = FileManager()

    def move_mouse(self, request):
        data = request.get_json()
        x, y = data.get("x"), data.get("y")
        self.mouse.move(x, y)
        return {"status": "ok"}

    def keyboard_type(self, request):
        data = request.get_json()
        text = data.get("text")
        self.keyboard.type(text)
        return {"status": "ok"}

    def media_play(self, request):
        self.media.play_pause()
        return {"status": "ok"}

    def file_open(self, request):
        data = request.get_json()
        path = data.get("path")
        self.file_manager.open(path)
        return {"status": "ok"}
