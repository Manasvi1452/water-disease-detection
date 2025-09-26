from flask import Flask, jsonify, render_template, request
import json
import os
from disease_prediction import predict_disease

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("disease_results.html")

@app.route("/api/sensors")
def get_sensors():
    json_path = os.path.join(app.static_folder, "disease_risk_sensors.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    return jsonify(data)


# New route for prediction
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    pH = float(data.get("sensor1"))
    turbidity = float(data.get("sensor2"))
    micro_count = float(data.get("sensor3"))
    rainfall = float(data.get("sensor4", 0))  # Default to 0 if not provided
    chlorine = float(data.get("chlorine", 0)) # Default to 0 if not provided
    result = predict_disease(pH, turbidity, micro_count, rainfall, chlorine)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
