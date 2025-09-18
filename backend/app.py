from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pickle
import numpy as np
import mysql.connector

app = Flask(__name__)
app.secret_key = '1234567890'

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '#Follow3Blues',
    'database': 'predictive_maintenance'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Load models and preprocessing tools
with open('ml_model/failure_model.pkl', 'rb') as f:
    failure_model = pickle.load(f)

with open('ml_model/time_model.pkl', 'rb') as f:
    time_model = pickle.load(f)

with open('ml_model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('ml_model/pca.pkl', 'rb') as f:
    pca = pickle.load(f)

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    product = session.get('product', 'Machine')
    return render_template('index.html', product=product)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([
        float(data['footfall']),
        float(data['tempMode']),
        float(data['AQ']),
        float(data['USS']),
        float(data['CS']),
        float(data['VOC']),
        float(data['RP']),
        float(data['IP']),
        float(data['Temperature'])
    ]).reshape(1, -1)

    # Preprocessing
    features_scaled = scaler.transform(features)
    features_pca = pca.transform(features_scaled)

    failure_prediction = int(failure_model.predict(features_pca)[0])

    if failure_prediction == 1:
        time_prediction = max(0, int(time_model.predict(features_pca)[0]))
        return jsonify({'prediction': f"Estimated failure in {time_prediction} hours."})
    else:
        return jsonify({'prediction': "Machine is operating normally."})

@app.route('/accuracy')
def get_accuracy():
    try:
        with open('ml_model/accuracy.txt', 'r') as f:
            accuracy = f.read()
    except FileNotFoundError:
        accuracy = "Unavailable"
    return jsonify({'accuracy': accuracy})

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    product = request.form['product']

    # Dummy user check
    if username == 'admin' and password == '1234':
        session['user'] = username
        session['product'] = product
        return redirect(url_for('home'))
    else:
        return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
