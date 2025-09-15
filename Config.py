import os


class Config:
    HOST = '0.0.0.0'
    PORT = 5000
    API_TOKEN = os.environ.get('PHONE_MOUSE_API_TOKEN', 'troco-esse-token-por-um-seguro')
    UPLOAD_DIR = os.environ.get('PHONE_MOUSE_UPLOAD_DIR', '/tmp/phone_mouse_uploads')
    MOUSE_SENSITIVITY = float(os.environ.get('PHONE_MOUSE_SENSITIVITY', '1.0'))
