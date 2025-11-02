import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear carpeta si no existe
os.makedirs('visualizations', exist_ok=True)

# Cargar datos
df = pd.read_csv('data/final_data.csv')
df = df.dropna(subset=['pickup_latitude', 'pickup_longitude'])

# Aplicar K-anonymity con redondeo agresivo
df['lat_anon'] = df['pickup_latitude'].round(2)
df['lon_anon'] = df['pickup_longitude'].round(2)

# Agrupar por coordenadas anonimizadas y contar frecuencia
grouped = df.groupby(['lat_anon', 'lon_anon']).size().reset_index(name='count')

# Graficar solo los grupos únicos
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    grouped['lon_anon'], grouped['lat_anon'],
    c=grouped['count'], cmap='viridis', s=100, alpha=0.8
)
plt.colorbar(scatter, label='Cantidad de puntos por grupo')
plt.title('K-anonymity: Agrupación de coordenadas anonimizadas')
plt.xlabel('Longitud (anonimizada)')
plt.ylabel('Latitud (anonimizada)')
plt.grid(True)

# Guardar gráfico
plt.savefig('visualizations/k_anonymity_grouped.png')
plt.close()

print("✅ Gráfico guardado en 'visualizations/k_anonymity_grouped.png'")