from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ml_model.predict import predict_failure

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))  # Ensure only logged-in users access index
    product = session.get('product', 'Unknown Product')
    return render_template('index.html', product=product)

@app_routes.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = [
        float(data['footfall']),
        float(data['tempMode']),
        float(data['AQ']),
        float(data['USS']),
        float(data['CS']),
        float(data['VOC']),
        float(data['RP']),
        float(data['IP']),
        float(data['Temperature'])
    ]

    result = predict_failure(features)
    return jsonify({'prediction': result})
