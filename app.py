from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Load model and encoders
model = None
le_crop = None
le_year = None
le_variety = None
le_state = None
le_season = None
le_zone = None

unique_crops = []
unique_years = []
unique_varieties = []
unique_states = []
unique_seasons = []
unique_zones = []

def load_resources():
    global model, le_crop, le_year, le_variety, le_state, le_season, le_zone
    global unique_crops, unique_years, unique_varieties, unique_states, unique_seasons, unique_zones
    try:
        model = joblib.load('model_full.pkl')
        le_crop = joblib.load('le_crop_full.pkl')
        le_year = joblib.load('le_year_full.pkl')
        le_variety = joblib.load('le_variety_full.pkl')
        le_state = joblib.load('le_state_full.pkl')
        le_season = joblib.load('le_season_full.pkl')
        le_zone = joblib.load('le_zone_full.pkl')
        
        unique_crops = list(le_crop.classes_)
        unique_years = list(le_year.classes_)
        unique_varieties = list(le_variety.classes_)
        unique_states = list(le_state.classes_)
        unique_seasons = list(le_season.classes_)
        unique_zones = list(le_zone.classes_)
        print("Resources loaded successfully.")
    except Exception as e:
        print(f"Error loading resources: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    return jsonify({
        'crops': unique_crops,
        'years': unique_years,
        'varieties': unique_varieties,
        'states': unique_states,
        'seasons': unique_seasons,
        'zones': unique_zones
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        data = request.json
        crop = data.get('crop')
        year = data.get('year')
        variety = data.get('variety')
        state = data.get('state')
        season = data.get('season')
        zone = data.get('zone')
        
        area = float(data.get('area', 0))
        yield_val = float(data.get('yield', 0))
        cost = float(data.get('cost', 0))
        
        # Encoding
        crop_enc = le_crop.transform([crop])[0] if crop in le_crop.classes_ else 0
        year_enc = le_year.transform([year])[0] if year in le_year.classes_ else 0
        variety_enc = le_variety.transform([variety])[0] if variety in le_variety.classes_ else 0
        state_enc = le_state.transform([state])[0] if state in le_state.classes_ else 0
        season_enc = le_season.transform([season])[0] if season in le_season.classes_ else 0
        zone_enc = le_zone.transform([zone])[0] if zone in le_zone.classes_ else 0
        
        # features = ['Crop_Encoded', 'Year_Encoded', 'Variety_Encoded', 'State_Encoded', 'Season_Encoded', 'Zone_Encoded', 'Cost', 'Area', 'Quantity']
        features = pd.DataFrame([[crop_enc, year_enc, variety_enc, state_enc, season_enc, zone_enc, cost, area, yield_val]], 
                                columns=['Crop_Encoded', 'Year_Encoded', 'Variety_Encoded', 'State_Encoded', 'Season_Encoded', 'Zone_Encoded', 'Cost', 'Area', 'Quantity'])
        
        prediction = model.predict(features)[0]
        
        # Generate AI Insight for Farmer
        insight = f"""
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <p><strong>Analysis for {variety} in {state}:</strong> Based on your inputs, the model predicts {round(prediction, 2)} Tons.</p>
        """
        
        yield_per_hectare = prediction / area if area > 0 else 0
        if yield_per_hectare > yield_val:
            insight += f"""
            <div style="background: rgba(16, 185, 129, 0.2); padding: 10px; border-radius: 5px;">
                <strong>✅ Excellent Projection!</strong> Your expected yield is tracking above average for the {season} season in {zone}.
            </div>
            <ul style="margin-left: 20px; text-align: left;">
                <li><strong>Soil Health:</strong> Continue your current soil nutrition strategy.</li>
                <li><strong>Cost Efficiency:</strong> At ₹{cost}/Quintal, your production scale is optimal.</li>
            </ul>
            """
        else:
            insight += f"""
            <div style="background: rgba(239, 68, 68, 0.2); padding: 10px; border-radius: 5px;">
                <strong>⚠️ Efficiency Warning</strong> Your projection is slightly below the regional average for {zone} during {season}.
            </div>
            <ul style="margin-left: 20px; text-align: left;">
                <li><strong>Resource Optimization:</strong> Re-evaluate your ₹{cost}/Quintal expenditure. Consider subsidized fertilizers.</li>
                <li><strong>Agronomy Tip:</strong> Ensure proper irrigation scheduling and monitor for localized pest threats.</li>
            </ul>
            """
            
        insight += "</div>"

        return jsonify({
            'prediction': round(float(prediction), 2),
            'insight': insight
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    load_resources()
    app.run(debug=True, port=5000)
