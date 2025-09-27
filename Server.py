from flask import Flask
from Controller import Controller

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.controller = Controller()
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule("/mouse/move", "move_mouse", self.controller.move_mouse, methods=["POST"])
        self.app.add_url_rule("/keyboard/type", "keyboard_type", self.controller.keyboard_type, methods=["POST"])
        self.app.add_url_rule("/media/play", "media_play", self.controller.media_play, methods=["POST"])
        self.app.add_url_rule("/file/open", "file_open", self.controller.file_open, methods=["POST"])

    def start(self, host="0.0.0.0", port=5000):
        self.app.run(host=host, port=port)
