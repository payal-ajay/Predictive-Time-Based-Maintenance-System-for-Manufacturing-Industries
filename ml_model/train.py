import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from backend.database import get_db_connection

# Load data
conn = get_db_connection()
query = "SELECT footfall, tempMode, AQ, USS, CS, VOC, RP, IP, Temperature, fail FROM machine_data"
df = pd.read_sql(query, conn)
conn.close()

# Split features and target
X = df[['footfall', 'tempMode', 'AQ', 'USS', 'CS', 'VOC', 'RP', 'IP', 'Temperature']]
y_fail = df['fail']

# Step 1: Scaling the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 2: Applying PCA
pca = PCA(n_components=0.95)  
X_pca = pca.fit_transform(X_scaled)

# Step 3: Training failure prediction model
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_fail, test_size=0.2, random_state=42)
failure_model = LogisticRegression(max_iter=200)
failure_model.fit(X_train, y_train)

# Step 4: Training time-to-failure model (only on failed data)
X_fail = X_pca[y_fail == 1]
y_time = np.random.randint(1, 100, size=len(X_fail))  
time_model = LinearRegression()
time_model.fit(X_fail, y_time)

# Step 5: Saving all the models
os.makedirs('ml_model', exist_ok=True)
with open('ml_model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('ml_model/pca.pkl', 'wb') as f:
    pickle.dump(pca, f)
with open('ml_model/failure_model.pkl', 'wb') as f:
    pickle.dump(failure_model, f)
with open('ml_model/time_model.pkl', 'wb') as f:
    pickle.dump(time_model, f)

print("Training completed and all models saved with PCA.")
y_pred = failure_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred) * 100
print(f"Failure prediction model accuracy: {accuracy:.2f}%")

# Saving accuracy to a file
with open('ml_model/accuracy.txt', 'w') as f:
    f.write(f"{accuracy:.2f}")