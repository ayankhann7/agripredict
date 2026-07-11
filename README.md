# AgriPredict AI 🌱

AgriPredict AI is a machine learning-powered web application designed to predict agricultural crop production in India. By analyzing historical data—including crop varieties, geographical zones, seasons, and cultivation costs—the AI provides an accurate production forecast and actionable agronomic insights for farmers.

## Features
- **Accurate Yield Forecasting**: Predicts total crop production using a Random Forest Regressor trained on extensive Indian agricultural data.
- **Interactive UI**: A fully responsive, modern web interface featuring a sleek, glassmorphism-inspired side-by-side dashboard.
- **Dynamic Data**: Dropdowns for states, crop varieties, and seasons are automatically populated from the trained machine learning model.
- **AI Farmer Insights**: Generates customized, interactive recommendations for resource optimization and soil health based on the farmer's specific inputs.

## Technologies Used
- **Backend**: Python, Flask, Flask-CORS
- **Machine Learning**: Scikit-Learn (Random Forest Regressor), Pandas, NumPy, Joblib
- **Frontend**: HTML5, Vanilla CSS (CSS Grid), Vanilla JavaScript

## Dataset Information
The model synthesizes and learns from **real agricultural datasets sourced from the Government of India ([data.gov.in](https://data.gov.in/))**. The historical data spans across the years **2001 to 2014**, providing a highly accurate baseline for modern predictions.

The dataset includes:
- Crop types and subsidiary varieties
- States and recommended cultivation zones
- Seasons and crop duration
- Cost of production (₹/Quintal C2)
- Historical area and yield metrics

## How to Run Locally

### Prerequisites
Make sure you have Python installed on your system.

### 1. Clone the repository
```bash
git clone https://github.com/ayankhann7/agripredict.git
cd agripredict
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install flask flask-cors pandas numpy scikit-learn joblib xgboost
```

### 3. Run the application
Start the Flask backend server:
```bash
python app.py
```

### 4. View the App
Open your web browser and navigate to:
`http://localhost:5000`

---
*Empowering Indian agriculture with predictive intelligence.*
