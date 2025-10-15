from App import app
from Hardware import ArduinoController

def main():
    arduino = ArduinoController(port="COM3", baudrate=9600)
    arduino.start_listening()
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
