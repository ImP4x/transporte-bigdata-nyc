import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_csv('data/yellow_tripdata_2015-01.csv', low_memory=False)

# Convertir fechas a formato datetime
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

# Calcular duración del viaje en segundos
df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()

# Eliminar nulos
df.dropna(inplace=True)

# Filtrar outliers (ejemplo: duración de viaje mayor a 3 horas)
df = df[df['trip_duration'] < 10800]

# Normalizar distancia
df['normalized_distance'] = (df['trip_distance'] - df['trip_distance'].mean()) / df['trip_distance'].std()

# Guardar datos limpios
df.to_csv('data/cleaned_data.csv', index=False)