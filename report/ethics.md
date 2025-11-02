# Evaluación Ética del Proyecto Big Data: Transporte Urbano

## 1. Riesgos de Privacidad

El dataset incluye coordenadas GPS de origen y destino, lo que puede revelar patrones de movilidad de personas. Esto representa un riesgo si los datos no se anonimizan adecuadamente.

**Ejemplo de riesgo**: Identificar la ubicación de una persona que toma taxis desde su casa cada mañana.

## 2. Soluciones Propuestas

Para mitigar estos riesgos, se aplicaron las siguientes técnicas:

- **Anonimización de coordenadas**: Se redondearon latitudes y longitudes a 3 decimales para evitar precisión exacta.
- **k-anonymity**: Se agruparon viajes por zonas y horarios para asegurar que cada dato represente al menos a k usuarios.
- **Eliminación de identificadores únicos**: No se usaron IDs de viaje ni placas de vehículos.

## 3. Sesgos en el Dataset

El dataset proviene exclusivamente de taxis en Nueva York, lo que introduce sesgos:

- **Geográficos**: No representa ciudades con diferente infraestructura o comportamiento de transporte.
- **Socioeconómicos**: Los datos pueden estar sesgados hacia zonas con mayor actividad comercial o turística.

## 4. Recomendaciones Éticas

- **Ampliar fuentes**: Usar datasets de otras ciudades o tipos de transporte (buses, bicicletas).
- **Evaluar equidad del modelo**: Verificar que las predicciones no favorezcan zonas específicas.
- **Cumplir con GDPR y principios de privacidad**: Aunque el proyecto es académico, se simulan prácticas responsables.

## 5. Conclusión

El proyecto busca generar insights útiles sin comprometer la privacidad de los usuarios. Se aplicaron medidas de anonimización y se reconocieron los límites del dataset para evitar conclusiones injustas o sesgadas.