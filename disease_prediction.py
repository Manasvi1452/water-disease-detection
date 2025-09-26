import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Generate synthetic dataset
np.random.seed(42)
n = 10000
pH = np.random.uniform(6.0, 9.0, n)
turbidity = np.random.uniform(0, 100, n)
microorganisms_count = np.random.poisson(20, n)
rainfall = np.random.uniform(0, 200, n)
chlorine = np.random.uniform(0.1, 2.0, n)

# Update risk score to include chlorine (lower chlorine = higher risk)
risk_score = (turbidity / 100) + (microorganisms_count / 100) + np.abs(pH - 7) / 3 + (rainfall / 200) + (1.5 - chlorine)
waterborne_disease = (risk_score > 0.5).astype(int)

data = pd.DataFrame({
    'pH': pH,
    'turbidity': turbidity,
    'microorganisms_count': microorganisms_count,
    'rainfall': rainfall,
    'chlorine': chlorine,
    'waterborne_disease': waterborne_disease
})

# Split data into train and test sets
X = data.drop('waterborne_disease', axis=1)
y = data['waterborne_disease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Example: Predict waterborne disease risk for new sample
def predict_disease(pH_val, turbidity_val, micro_count_val, rainfall_val, chlorine_val):
    sample = np.array([[pH_val, turbidity_val, micro_count_val, rainfall_val, chlorine_val]])
    prediction = model.predict(sample)
    return "Disease Risk" if prediction[0] == 1 else "No Disease Risk"

# Example usage
print(predict_disease(8.5, 90, 50, 180, 0.5))
# Batch sensor input example
sensor_readings = [
    # (pH, turbidity, microorganisms_count, rainfall, chlorine)
    (7.0, 10, 5, 10, 1.5),      # No Disease Risk
    (8.5, 90, 50, 180, 0.2),    # Disease Risk
    (6.2, 80, 40, 150, 0.3),    # Disease Risk
    (7.1, 20, 10, 30, 1.2),     # No Disease Risk
    (8.0, 95, 60, 190, 0.1),    # Disease Risk
]

print("Sensors with Disease Risk:")
for idx, (pH, turbidity, micro_count, rainfall, chlorine) in enumerate(sensor_readings, 1):
    result = predict_disease(pH, turbidity, micro_count, rainfall, chlorine)
    if result == "Disease Risk":
        print(f"Sensor {idx}: pH={pH}, turbidity={turbidity}, microorganisms_count={micro_count}, rainfall={rainfall}, chlorine={chlorine}")
