from flask import Flask, request, jsonify
from MouseApi.actions.MouseAnalyzer import MouseAnalyzer


analyzer = MouseAnalyzer()
app = Flask(__name__)

@app.route("/telemetry/mouse/data", methods=["POST"])
def telemetry_data():
    try:
        data = request.get_json(force=True)
        if isinstance(data, list):
            added = [analyzer.add_sample(d) for d in data]
            return jsonify({"received": len(added)}), 200
        else:
            added = analyzer.add_sample(data)
            return jsonify(added), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/telemetry/mouse/stats", methods=["GET"])
def telemetry_stats():
    return jsonify(analyzer.summary())

@app.route("/telemetry/mouse/clear", methods=["POST"])
def telemetry_clear():
    analyzer.clear()
    return jsonify({"status": "cleared"}), 200

def run_telemetry(host="0.0.0.0", port=6000):
    print(f"[INFO] Iniciando Telemetry Server em http://{host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_telemetry()