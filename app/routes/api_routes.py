from flask import Blueprint, request, jsonify
from app.modules.database import insert_prediction
import pickle
from config import Config
import pandas as pd
import os
import sys

# Adjust the path to access the config file from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Define the blueprint for the API
api_bp = Blueprint('api_bp', __name__)

# Load your model
# Checks if the model exists
if os.path.exists(Config.MODEL_PATH):
    with open(Config.MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)

    with open('app/ai-model/label_encoder_pnns.pkl', "rb") as label_encoder_file:
        label_encoder_pnns = pickle.load(label_encoder_file)

    with open('app/ai-model/ordinal_encoder_grade.pkl', "rb") as ordinal_encoder_file:
        ordinal_encoder_grade = pickle.load(ordinal_encoder_file)

    with open('app/ai-model/scaler.pkl', "rb") as scaler_file:
        scaler = pickle.load(scaler_file)

@api_bp.route('/api/v1/predict-nutriscore', methods=['POST'])
def predict_nutriscore():
    try:
        data = request.get_json()

        # Check for missing features and create DataFrame
        features = ["pnns_groups_1", "energy-kcal_100g", "fat_100g", "saturated-fat_100g", 
                    "sugars_100g", "fiber_100g", "proteins_100g", "salt_100g", 
                    "sodium_100g", "fruits-vegetables-nuts-estimate-from-ingredients_100g"]

        for feature in features:
            if feature not in data:
                return jsonify({"error": f"Missing feature: {feature}"}), 400

        input_data = pd.DataFrame([data])

        # Encode 'pnns_groups_1' using the label encoder
        input_data["pnns_groups_1"] = label_encoder_pnns.transform(input_data["pnns_groups_1"])

        # Scale numerical features
        input_data_scaled = scaler.transform(input_data)

        # Predict Nutri-Score grade
        prediction = model.predict(input_data_scaled)[0]

        # Decode the prediction if necessary
        prediction_grade = ordinal_encoder_grade.inverse_transform([[prediction]])[0][0]

        data = request.get_json()  # Collect data from JSON payload

        insert_prediction(data, prediction_grade)

        return jsonify({"nutriscore_grade": prediction_grade})

    except Exception as e:
        return jsonify({"error": str(e)}), 500