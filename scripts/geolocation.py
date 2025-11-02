import pandas as pd
import requests
import time

API_KEY = '99bf1bf52eaf4ce1b7d5adc12167faa4'  # Reemplaza si generas una nueva
URL = 'https://api.opencagedata.com/geocode/v1/json'

# Cargar datos enriquecidos con clima y tomar muestra
df = pd.read_csv('data/enriched_data.csv').sample(100, random_state=42)

# Crear columna para zona geográfica
zones = []

for index, row in df.iterrows():
    lat = row['pickup_latitude']
    lon = row['pickup_longitude']

    print(f"Procesando fila {index} - lat: {lat}, lon: {lon}")

    params = {
        'q': f'{lat},{lon}',
        'key': API_KEY,
        'language': 'es',
        'no_annotations': 1
    }

    try:
        response = requests.get(URL, params=params)
        data = response.json()
        components = data['results'][0]['components']
        zona = components.get('neighbourhood') or components.get('suburb') or components.get('city') or 'Desconocido'
    except Exception as e:
        print(f"Error en fila {index}: {e}")
        zona = 'Error'

    zones.append(zona)
    time.sleep(1)  # Respeta el límite de la API

# Agregar columna al DataFrame
df['zone'] = zones

# Guardar archivo final
df.to_csv('data/final_data.csv', index=False)
print("✅ Archivo final_data.csv guardado correctamente con zonas geográficas.")