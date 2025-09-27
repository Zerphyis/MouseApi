from flask import request
from actions.MouseAction import MouseAction
from actions.KeyBoardAction import KeyBoardAction
from actions.MediaAction import MediaAction
from actions.FileManager import FileManager
from HandleController import HandleController

handle_controller = HandleController()

class Controller:
    def __init__(self):
        self.mouse = MouseAction()
        self.keyboard = KeyBoardAction()
        self.media = MediaAction()
        self.file_manager = FileManager()

    @handle_controller.handle
    def move_mouse(self):
        data = request.get_json()
        x, y = data.get("x"), data.get("y")
        self.mouse.move(x, y)
        return {"status": "ok"}

    @handle_controller.handle
    def keyboard_type(self):
        data = request.get_json()
        text = data.get("text")
        self.keyboard.type(text)
        return {"status": "ok"}

    @handle_controller.handle
    def media_play(self):
        self.media.play_pause()
        return {"status": "ok"}

    @handle_controller.handle
    def file_open(self):
        data = request.get_json()
        path = data.get("path")
        self.file_manager.open(path)
        return {"status": "ok"}
