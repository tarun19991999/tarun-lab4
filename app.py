from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model and scaler
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# API endpoint for prediction
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input values from request
        data = request.form
        length1 = float(data["length1"])
        length2 = float(data["length2"])
        length3 = float(data["length3"])
        height = float(data["height"])
        width = float(data["width"])

        # One-hot encoding for species selection
        species = data["species"]
        species_cols = ['Species_Parkki', 'Species_Perch', 'Species_Pike', 
                        'Species_Roach', 'Species_Smelt', 'Species_Whitefish']
        species_data = [1 if species == col.split('_')[1] else 0 for col in species_cols]

        # Create input array
        input_data = np.array([[length1, length2, length3, height, width] + species_data])

        # Standardize input data
        input_scaled = scaler.transform(input_data)

        # Make prediction
        predicted_weight = model.predict(input_scaled)[0]

        return jsonify({"Predicted Weight": round(predicted_weight, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
