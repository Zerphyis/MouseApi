from flask import Flask, request, jsonify, send_file, abort
import io
import time
from .config import Config
from .auth import Auth
from .controller import InputController
from .file_manager import FileManager
from .actions.mouse_action import MouseAction
from .actions.keyboard_action import KeyboardAction
from .actions.media_action import MediaAction


class APIServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.ctrl = InputController()
        self.mouse = MouseAction(self.ctrl)
        self.keyboard = KeyboardAction(self.ctrl)
        self.media = MediaAction(self.ctrl)
        self.files = FileManager(Config.UPLOAD_DIR)
        self._register_routes()

    def _require_auth(self):
        if not Auth.check_request(request):
            abort(401, description='Unauthorized')

    def _register_routes(self):
        app = self.app

        @app.route('/ping')
        def ping():
            return jsonify({'ok': True, 'time': time.time()})

        @app.route('/mouse/move', methods=['POST'])
        def move_mouse():
            self._require_auth()
            data = request.json
            dx = data.get('dx', 0)
            dy = data.get('dy', 0)
            absolute = data.get('absolute', False)
            try:
                self.ctrl.move_mouse(dx, dy, absolute)
                return jsonify({'ok': True})
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

        @app.route('/mouse/click', methods=['POST'])
        def click_mouse():
            self._require_auth()
            data = request.json
            button = data.get('button', 'left')
            clicks = data.get('clicks', 1)
            interval = data.get('interval', 0.0)
            try:
                self.ctrl.click(button, clicks, interval)
                return jsonify({'ok': True})
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

        @app.route('/mouse/scroll', methods=['POST'])
        def scroll_mouse():
            self._require_auth()
            data = request.json
            amount = data.get('amount', 0)
            try:
                self.ctrl.scroll(amount)
                return jsonify({'ok': True})
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

        @app.route('/keyboard/press', methods=['POST'])
        def press_key():
            self._require_auth()
            data = request.json
            key = data.get('key')
            if not key:
                return jsonify({'ok': False, 'error': 'Missing key'}), 400
            try:
                self.ctrl.press_key(key)
                return jsonify({'ok': True})
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

        @app.route('/keyboard/hotkey', methods=['POST'])
        def hotkey():
            self._require_auth()
            data = request.json
            keys = data.get('keys', [])
            if not keys:
                return jsonify({'ok': False, 'error': 'Missing keys'}), 400
            try:
                self.ctrl.hotkey(*keys)
                return jsonify({'ok': True})
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

        @app.route('/keyboard/type', methods=['POST'])
        def type_text():
            self._require_auth()
            data = request.json
            text = data.get('text', '')
            interval = data.get('interval', 0.0)
            try:
                self.ctrl.type_text(text, interval)
                return jsonify({'ok': True})
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

        @app.route('/screenshot', methods=['GET'])
        def screenshot():
            self._require_auth()
            x = request.args.get('x', type=int)
            y = request.args.get('y', type=int)
            w = request.args.get('w', type=int)
            h = request.args.get('h', type=int)
            region = (x, y, w, h) if all(v is not None for v in [x, y, w, h]) else None
            try:
                img_bytes = self.ctrl.screenshot(region)
                return send_file(io.BytesIO(img_bytes), mimetype='image/png')
            except RuntimeError as e:
                return jsonify({'ok': False, 'error': str(e)}), 400

    def run(self):
        print(f'[INFO] Running on {Config.HOST}:{Config.PORT}')
        self.app.run(host=Config.HOST, port=Config.PORT)
