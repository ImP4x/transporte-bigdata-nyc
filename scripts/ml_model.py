import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cargar datos
import time
start = time.time()
df = pd.read_csv('data/cleaned_data.csv').sample(5000, random_state=42)
print("Tiempo de carga:", round(time.time() - start, 2), "segundos")

# Variables
X = df[['trip_distance']]
y = df['trip_duration']

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Modelo 1: Regresión Lineal
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# 🔹 Modelo 2: Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# 🔸 Métricas
def print_metrics(name, y_true, y_pred):
    print(f"\n📊 {name}")
    print("MAE:", round(mean_absolute_error(y_true, y_pred), 2))
    print("RMSE:", round(np.sqrt(mean_squared_error(y_true, y_pred)), 2))
    print("R²:", round(r2_score(y_true, y_pred), 4))

print_metrics("Regresión Lineal", y_test, y_pred_lr)
print_metrics("Random Forest", y_test, y_pred_rf)

# 🔸 Visualización de errores
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred_lr, label='Linear Regression', alpha=0.6)
sns.scatterplot(x=y_test, y=y_pred_rf, label='Random Forest', alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel("Duración real (s)")
plt.ylabel("Duración predicha (s)")
plt.title("Comparación de predicciones")
plt.legend()
plt.tight_layout()
import os
os.makedirs('visualizations', exist_ok=True)
plt.savefig('visualizations/prediction_comparison.png')
#plt.show()