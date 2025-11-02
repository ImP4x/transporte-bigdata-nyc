import pandas as pd
import requests
import time

API_KEY = '03e7315f31bdf0b0a36282e330785cf2'
URL = 'https://api.openweathermap.org/data/2.5/weather'

# Cargar datos limpios y tomar una muestra de 500 filas
df = pd.read_csv('data/cleaned_data.csv').sample(500, random_state=42)

# Crear columna para clima
weather_data = []

for index, row in df.iterrows():
    lat = row['pickup_latitude']
    lon = row['pickup_longitude']

    print(f"Procesando fila {index} - lat: {lat}, lon: {lon}")  # Diagnóstico

    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(URL, params=params)
        data = response.json()
        weather = data.get('weather', [{}])[0].get('main', 'Unknown')
    except Exception as e:
        print(f"Error en fila {index}: {e}")
        weather = 'Error'

    weather_data.append(weather)
    time.sleep(1)  # Evita sobrecargar la API

# Agregar columna al DataFrame
df['weather'] = weather_data

# 🔹 Asignar zona urbana según coordenadas
def asignar_zona(lat, lon):
    if 40.74 < lat < 40.77 and -74.01 < lon < -73.98:
        return 'Midtown Manhattan'
    elif 40.70 < lat < 40.73 and -74.01 < lon < -73.97:
        return 'Lower Manhattan'
    elif 40.75 < lat < 40.78 and -73.90 < lon < -73.85:
        return 'Queens'
    elif 40.85 < lat < 40.90 and -73.90 < lon < -73.85:
        return 'Bronx Norte'
    else:
        return 'Otra'

df['zone'] = df.apply(lambda row: asignar_zona(row['pickup_latitude'], row['pickup_longitude']), axis=1)

# Guardar archivo enriquecido
df.to_csv('data/enriched_data.csv', index=False)
print("✅ Archivo enriched_data.csv guardado correctamente con columnas 'weather' y 'zone'.")