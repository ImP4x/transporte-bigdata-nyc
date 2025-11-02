import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# ✅ SOLUCIÓN: Detectar la ruta base automáticamente para local y cloud
BASE_DIR = Path(__file__).parent.parent
if str(BASE_DIR).endswith('dashboard'):
    BASE_DIR = BASE_DIR.parent
else:
    BASE_DIR = Path.cwd()

DATA_DIR = BASE_DIR / "data"
VIZ_DIR = BASE_DIR / "visualizations"


# Configuración de página con diseño moderno
st.set_page_config(
    page_title="Análisis de Transporte Urbano - NYC",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)




# CSS personalizado con diseño moderno en azul
st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Fondo general con gradiente OSCURO */
    .main {
        background: linear-gradient(135deg, #0A0E27 0%, #151B3B 50%, #0A0E27 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Fondo del área de contenido principal OSCURO */
    .block-container {
        background-color: #0D1117;
        padding: 2rem 1rem;
    }
    
    /* Fondo de toda la aplicación OSCURO */
    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #0D1117 50%, #0A0E27 100%);
    }
    
    /* Animación de fade-in */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Título principal con gradiente */
    h1 {
        background: linear-gradient(135deg, #00BFFF 0%, #0066FF 50%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        padding: 20px 0;
        animation: fadeIn 0.8s ease-out;
        text-align: center;
    }
    
    /* Headers con estilo moderno */
    h2 {
        color: #00BFFF !important;
        font-weight: 600;
        padding: 20px 0 15px 0;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #00BFFF, #0066FF, transparent) 1;
        animation: fadeIn 0.6s ease-out;
    }
    
    h3 {
        color: #A0AEC0 !important;
        font-weight: 500;
    }
    
    /* Cajas de información con glassmorphism */
    .info-box {
        background: linear-gradient(135deg, rgba(21, 27, 59, 0.7), rgba(10, 14, 39, 0.8));
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(0, 191, 255, 0.3);
        margin: 15px 0;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 191, 255, 0.15);
        animation: fadeIn 0.7s ease-out;
    }
    
    /* Sidebar mejorado */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0E27 0%, #151B3B 50%, #0A0E27 100%);
        border-right: 2px solid rgba(0, 191, 255, 0.2);
    }
    
    /* Tabs modernos */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(21, 27, 59, 0.5);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 10px 25px;
        background: linear-gradient(135deg, rgba(21, 27, 59, 0.8), rgba(10, 14, 39, 0.9));
        border-radius: 10px;
        border: 1px solid rgba(0, 191, 255, 0.2);
        color: #A0AEC0;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 102, 255, 0.2));
        border-color: rgba(0, 191, 255, 0.5);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00BFFF, #0066FF) !important;
        border-color: #00F0FF !important;
        color: #FFFFFF !important;
        box-shadow: 0 5px 20px rgba(0, 191, 255, 0.4);
    }
    
    /* Imágenes con efecto hover */
    img {
        border-radius: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 191, 255, 0.2);
    }
    
    img:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 40px rgba(0, 191, 255, 0.4);
    }
    
    /* Selectbox mejorado */
    .stSelectbox [data-baseweb="select"] {
        background: rgba(21, 27, 59, 0.8);
        border: 1px solid rgba(0, 191, 255, 0.3);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    /* Dataframe con estilo */
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0, 191, 255, 0.15);
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A0E27;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00BFFF, #0066FF);
        border-radius: 5px;
    }
    
    /* Texto general */
    p, li, div {
        color: #A0AEC0;
    }
    
    /* Métricas visuales */
    [data-testid="stMetricValue"] {
        color: #00BFFF;
        font-size: 2rem;
        font-weight: 600;
    }
    
    /* Ocultar warnings de Streamlit */
    .stAlert {
        display: none;
    }
    
    /* Estilo para los dividers */
    hr {
        border-color: rgba(0, 191, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)




# Sidebar moderno
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 80px; animation: pulse 2s infinite;'>🚕</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #00BFFF; border: none;'>NYC Transport</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📋 Pipeline Completo")
    st.info("""
    **Tecnologías Big Data**
    
    ✅ Procesamiento masivo  
    ✅ Machine Learning  
    ✅ Visualizaciones avanzadas  
    ✅ Análisis con PySpark  
    ✅ Enriquecimiento con APIs  
    """)
    
    st.markdown("---")
    st.markdown("### 👥 Autores")
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 191, 255, 0.1), rgba(0, 102, 255, 0.1)); 
                padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 191, 255, 0.3);'>
        <b style='color: #00BFFF;'>👨‍💻 Carlos Ramos</b><br>
        <b style='color: #00BFFF;'>👨‍💻 Willian Lozada</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px;'>
            <p>🎓 Proyecto Big Data 2025</p>
            <p>📍 New York City</p>
        </div>
    """, unsafe_allow_html=True)




# Header principal
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <div style='font-size: 60px; animation: pulse 3s infinite;'>🚕</div>
    </div>
""", unsafe_allow_html=True)




st.title("Proyecto Final: Análisis y Predicción de Transporte Urbano")




st.markdown("""
<div class="info-box">
    <h3 style='color: #00BFFF; margin-top: 0;'>🎯 Sistema Completo de Análisis Big Data</h3>
    Este dashboard presenta un sistema completo de análisis de datos de transporte urbano de NYC,
    incluyendo <b>procesamiento Big Data</b>, <b>predicción con ML</b>, <b>visualización de patrones geoespaciales</b>, 
    y <b>análisis temporal con PySpark</b>.
</div>
""", unsafe_allow_html=True)




st.markdown("---")




# 🔹 Sección 1: Estadísticas generales - CON VALORES PREDETERMINADOS
st.header("📊 Estadísticas Generales")



# Valores predeterminados del dataset completo (cleaned_data.csv 2.3GB)
total_registros = 12_738_553
duracion_promedio = 736.45
distancia_promedio = 13.47



col1, col2, col3 = st.columns(3)



with col1:
    st.metric(
        label="📝 Número de registros",
        value=f"{total_registros:,}"
    )



with col2:
    st.metric(
        label="⏱️ Duración promedio de viaje (s)",
        value=f"{duracion_promedio}"
    )



with col3:
    st.metric(
        label="🛣️ Distancia promedio (km)",
        value=f"{distancia_promedio}"
    )



st.markdown("---")




# 🔹 Sección 2, 3, 4: Visualizaciones con tabs
st.header("📈 Análisis de Modelos y Visualizaciones")




tab1, tab2, tab3 = st.tabs(["🕒 Error por Hora", "🤖 Modelos ML", "🌆 Mapa de Calor"])




with tab1:
    st.subheader("Error de Predicción por Hora")
    st.markdown("""
    <div class='info-box' style='border-left: 5px solid #667eea;'>
        Este gráfico muestra cómo varía el <b>error absoluto promedio</b> de las predicciones
        según la hora del día, permitiendo identificar patrones temporales en la precisión del modelo.
    </div>
    """, unsafe_allow_html=True)
    
    try:
        st.image(str(VIZ_DIR / "error_por_hora.png"), 
                caption="Error absoluto promedio por hora del día",
                use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Imagen no encontrada: error_por_hora.png")




with tab2:
    st.subheader("Comparación de Modelos de ML")
    st.markdown("""
    <div class='info-box' style='border-left: 5px solid #00BFFF;'>
        Comparación visual entre las <b>predicciones del modelo</b> y la <b>duración real</b> de los viajes.
    </div>
    """, unsafe_allow_html=True)
    
    try:
        st.image(str(VIZ_DIR / "prediction_comparison.png"),
                caption="Predicción vs. duración real",
                use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Imagen no encontrada: prediction_comparison.png")




with tab3:
    st.subheader("Mapa de Calor de Viajes")
    st.markdown("""
    <div class='info-box' style='border-left: 5px solid #f5576c;'>
        Visualización <b>geoespacial de densidad</b> de viajes en NYC.
    </div>
    """, unsafe_allow_html=True)
    
    try:
        st.image(str(VIZ_DIR / "heatmap_nyc_log_annotated_clean.png"),
                caption="Densidad de viajes por zona (NYC)",
                use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Imagen no encontrada: heatmap_nyc_log_annotated_clean.png")




st.markdown("---")




# 🔹 Sección 5: Clima y zona (mejorada visualmente)
st.header("🌦️ Clima y Zona")




try:
    df_weather = pd.read_csv(str(DATA_DIR / "enriched_data.csv"))
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(21, 27, 59, 0.8), rgba(10, 14, 39, 0.9));
                    padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 191, 255, 0.3);'>
            <h3 style='color: #00BFFF; margin-top: 0;'>🎛️ Filtros</h3>
        </div>
        """, unsafe_allow_html=True)
        
        zona_seleccionada = st.selectbox("🗺️ Selecciona una zona:", df_weather['zone'].unique())
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0, 191, 255, 0.1), rgba(0, 102, 255, 0.1));
                    padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 191, 255, 0.3);'>
            <h3 style='color: #00BFFF; margin: 0;'>📍 Zona: <span style='color: #00F0FF;'>{zona_seleccionada}</span></h3>
        </div>
        """, unsafe_allow_html=True)
        
        df_filtrado = df_weather[df_weather['zone'] == zona_seleccionada]
        st.dataframe(df_filtrado[['pickup_latitude', 'pickup_longitude', 'weather']].head(), use_container_width=True)




except Exception as e:
    st.error(f"❌ Error al cargar datos de clima: {e}")




st.markdown("---")




# 🔹 Sección 6: Datos por hora (Spark)
st.header("⚡ Viajes por Hora (PySpark en Databricks)")




st.markdown("""
<div class="info-box">
    <h3 style='color: #667eea; margin-top: 0;'>🚀 Procesamiento Big Data Distribuido</h3>
    Este gráfico muestra la cantidad de viajes por hora del día, procesado en <b>Databricks</b> usando <b>PySpark</b>.
</div>
""", unsafe_allow_html=True)




try:
    df_hour = pd.read_csv(str(DATA_DIR / "trips_by_hour.csv"))
    st.bar_chart(df_hour.set_index('hour'))
except Exception as e:
    st.error(f"❌ Error al cargar datos por hora: {e}")




st.markdown("---")




# 🔹 Sección FINAL: Créditos simplificado
st.header("🎤 Presentación y Créditos")




col1, col2 = st.columns(2)




with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(21, 27, 59, 0.8), rgba(10, 14, 39, 0.9));
                padding: 20px; border-radius: 15px; border: 1px solid rgba(0, 191, 255, 0.3);'>
        <h3 style='color: #00BFFF;'>👥 Autores</h3>
        <p style='color: #A0AEC0; font-size: 16px;'>
            <b>Carlos Ramos</b><br>
            <b>Willian Lozada</b>
        </p>
    </div>
    """, unsafe_allow_html=True)




with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(21, 27, 59, 0.8), rgba(10, 14, 39, 0.9));
                padding: 20px; border-radius: 15px; border: 1px solid rgba(0, 191, 255, 0.3);'>
        <h3 style='color: #00BFFF;'>🎯 Demo</h3>
        <p style='color: #A0AEC0; font-size: 16px;'>
            <b>Duración:</b> 10–15 minutos<br>
            <b>Objetivo:</b> Pipeline completo, insights y visualizaciones
        </p>
    </div>
    """, unsafe_allow_html=True)




st.markdown("---")




# Footer
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(21, 27, 59, 0.8), rgba(10, 14, 39, 0.9));
            padding: 30px; border-radius: 15px; border: 1px solid rgba(0, 191, 255, 0.2); 
            text-align: center; margin-top: 40px;'>
    <p style='color: #00BFFF; font-size: 16px;'><b>🚕 NYC Urban Transport Analysis Dashboard</b></p>
    <p style='color: #A0AEC0; font-size: 14px;'>Big Data Project 2025 | Desarrollado con ❤️ usando Streamlit</p>
</div>
""", unsafe_allow_html=True)
