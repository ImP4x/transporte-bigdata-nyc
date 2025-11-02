import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import seaborn as sns
import matplotlib.pyplot as plt
import os
# Cargar datos limpios
df = pd.read_csv('data/cleaned_data.csv')

# Extraer hora del día
df['hour'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.hour

# Entrenar modelo simple
X = df[['trip_distance']]
y = df['trip_duration']
model = LinearRegression().fit(X, y)
df['predicted_duration'] = model.predict(X)

# Calcular error absoluto
df['abs_error'] = abs(df['trip_duration'] - df['predicted_duration'])

# Agrupar por hora
hourly_errors = df.groupby('hour')['abs_error'].mean().reset_index()

# Visualizar
plt.figure(figsize=(10, 6))
sns.lineplot(data=hourly_errors, x='hour', y='abs_error', marker='o', color='crimson')
plt.title("Error de predicción por hora del día")
plt.xlabel("Hora del día")
plt.ylabel("Error absoluto promedio (segundos)")
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()
# Crear carpeta si no existe
os.makedirs('../visualizations', exist_ok=True)
plt.savefig('visualizations/error_por_hora.png')
plt.show()