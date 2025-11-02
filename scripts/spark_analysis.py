from pyspark.sql import SparkSession

# Crear sesión de Spark
spark = SparkSession.builder.appName("TaxiAnalysis").getOrCreate()

# Cargar el dataset limpio
df = spark.read.csv("../data/cleaned_data.csv", header=True, inferSchema=True)

# Agrupar viajes por hora
df = df.withColumn("hour", df["tpep_pickup_datetime"].substr(12, 2))
hourly_counts = df.groupBy("hour").count().orderBy("hour")

# Mostrar resultado en consola
hourly_counts.show()

# 🔹 Guardar resultado como CSV para el dashboard
# Convertir a Pandas y guardar en carpeta data/
hourly_counts.toPandas().to_csv("../data/trips_by_hour.csv", index=False)

print("✅ Archivo trips_by_hour.csv guardado correctamente.")