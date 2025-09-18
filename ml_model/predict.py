import numpy as np
import pickle

def load_models():
    with open('ml_model/failure_model.pkl', 'rb') as f:
        failure_model = pickle.load(f)

    with open('ml_model/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    with open('ml_model/pca.pkl', 'rb') as f:
        pca = pickle.load(f)

    try:
        with open('ml_model/time_model.pkl', 'rb') as f:
            time_model = pickle.load(f)
    except FileNotFoundError:
        time_model = None

    return failure_model, time_model, scaler, pca

def predict_failure(features):
    failure_model, time_model, scaler, pca = load_models()

    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)
    features_pca = pca.transform(features_scaled)

    failure_prediction = int(failure_model.predict(features_pca)[0])

    if failure_prediction == 1 and time_model:
        estimated_hours = int(time_model.predict(features_pca)[0])
        return f"Estimated failure in {estimated_hours} hours"
    elif failure_prediction == 1:
        return "Failure expected, but time estimate unavailable"
    else:
        return "No failure expected"