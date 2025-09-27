from flask import Flask
from flask_socketio import SocketIO, emit

class WifiInterface:
    def __init__(self, port: int = 5000):
        self.port = port
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "mouseapi_secret"
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.clients = set()

        @self.socketio.on("connect")
        def handle_connect():
            self.clients.add("client")
            print("[Wifi] Cliente conectado")

        @self.socketio.on("disconnect")
        def handle_disconnect():
            if "client" in self.clients:
                self.clients.remove("client")
            print("[Wifi] Cliente desconectado")

    def start_server(self):
        """
        Inicia o servidor Flask-SocketIO.
        """
        print(f"[Wifi] Servidor iniciado na porta {self.port}")
        self.socketio.run(self.app, port=self.port)

    def send_message(self, data: dict):
        """
        Envia mensagem para todos os clientes conectados.
        """
        print(f"[Wifi] Enviando: {data}")
        self.socketio.emit("mouse_event", data)

    def stop_server(self):
        """
        Finaliza o servidor (força parada).
        """
        print("[Wifi] Servidor parado (CTRL+C para encerrar processo).")
