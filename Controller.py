from Config import BLUETOOTH_ENABLED, WIFI_ENABLED, BLUETOOTH_DEVICE_NAME, WIFI_PORT
from actions.MouseAnalyzer import MouseAnalyzer
from interfaces.BluetoothInterface import BluetoothInterface
from interfaces.WifiInterface import WifiInterface

class Controller:
    """
    Controlador principal. Faz a ponte entre:
    - Bluetooth (entrada de eventos)
    - Wifi (comunicação com celular/servidor)
    - MouseAnalyzer (análise de métricas)
    """

    def __init__(self):
        self.analyzer = MouseAnalyzer()
        self.bt = None
        self.wifi = None

        if BLUETOOTH_ENABLED:
            self.bt = BluetoothInterface(callback=self.handle_event)
        if WIFI_ENABLED:
            self.wifi = WifiInterface(port=WIFI_PORT)

    def start(self):
        """
        Inicia os serviços configurados.
        """
        if self.bt:
            self.bt.connect(BLUETOOTH_DEVICE_NAME)
        if self.wifi:
            # roda servidor socketio (bloqueante)
            self.wifi.start_server()

    def handle_event(self, event: dict):
        """
        Recebe evento (ex: movimento, clique) do mouse via Bluetooth.
        Analisa e envia resultado via Wifi.
        """
        result = None

        if event["type"] == "movement":
            result = self.analyzer.analyze_movement(event["dx"], event["dy"])
        elif event["type"] == "click":
            result = self.analyzer.analyze_click(event["button"])
        elif event["type"] == "lag":
            result = {"lag_ms": self.analyzer.analyze_input_lag(event["timestamp"])}

        if self.wifi and result:
            self.wifi.send_message(result)

        return result

    def stop(self):
        """
        Para os serviços.
        """
        if self.bt:
            self.bt.disconnect()
        if self.wifi:
            self.wifi.stop_server()
