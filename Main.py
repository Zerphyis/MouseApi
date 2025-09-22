from Server import APIServer
import threading

def start_telemetry():
    try:
        from . import mouse_telemetry_server
        t = threading.Thread(
            target=mouse_telemetry_server.run_telemetry,
            kwargs={"host": "0.0.0.0", "port": 6000},
            daemon=True
        )
        t.start()
        print("[INFO] Telemetry server iniciado em http://0.0.0.0:6000")
    except Exception as e:
        print("[WARN] Telemetry server não iniciado:", e)

def main():
    start_telemetry()
    server = APIServer()
    server.register_mouse_endpoints()
    server.run()

if __name__ == '__main__':
    main()
