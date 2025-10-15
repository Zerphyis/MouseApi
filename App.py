# App.py
from flask import Flask, request, jsonify
from Controller import Controller
from Hardware import ArduinoController

app = Flask(__name__)
controller = Controller()

@app.route("/mouse/move", methods=["POST"])
def move_mouse():
    controller.move_mouse(request)
    return jsonify({"status": "ok", "action": "move_mouse"})

@app.route("/mouse/click", methods=["POST"])
def click_mouse():
    controller.click_mouse(request)
    return jsonify({"status": "ok", "action": "click_mouse"})

@app.route("/mouse/scroll", methods=["POST"])
def scroll_mouse():
    controller.scroll_mouse(request)
    return jsonify({"status": "ok", "action": "scroll_mouse"})

if __name__ == "__main__":
    arduino = ArduinoController(port="COM3", baudrate=9600)
    arduino.start_listening()

    controller.set_arduino(arduino)

    app.run(host="0.0.0.0", port=5000)
