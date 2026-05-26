import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np
import time
import platform

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="SafeDrive AI - Monitor de Distracciones",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: 800; color: #0F172A; margin-bottom: 5px; }
    .subtitle { font-size: 16px; color: #475569; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 SafeDrive AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análisis de distracciones al volante optimizado.</p>', unsafe_allow_html=True)

# --- PANEL LATERAL ---
st.sidebar.title("Panel de Control")
st.sidebar.markdown("---")

@st.cache_resource
def load_model():
    return YOLO("best.pt")

try:
    model_dist = load_model()
    st.sidebar.success("🤖 Modelo 'best.pt' cargado")
except Exception as e:
    st.sidebar.error("❌ No se encontró 'best.pt'.")
    st.stop()

st.sidebar.subheader("⚙️ Parámetros del Modelo")
conf_threshold = st.sidebar.slider("Umbral de Confianza", min_value=0.05, max_value=1.0, value=0.25, step=0.05)

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["🎥 Cámara en Tiempo Real", "🖼️ Análisis de Imágenes Estáticas"])

# ==========================================
# PESTAÑA 1: VÍDEO EN TIEMPO REAL
# ==========================================
with tab1:
    col_cam, col_btn = st.columns([2, 1])
    with col_cam:
        cam_index = st.selectbox("Selecciona la fuente de vídeo:", options=[0, 1, 2, 3, 4], index=0)
    with col_btn:
        st.write("")
        st.write("")
        run_system = st.checkbox("🟢 Activar Cámara", value=False)

    FRAME_WINDOW = st.image([])

    if run_system:
        if platform.system() == 'Windows':
            cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(cam_index)
        
        # SOLUCIÓN: Forzar captura en alta resolución para evitar deformaciones previas
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        if not cap.isOpened():
            st.error(f"Error al abrir la cámara {cam_index}.")
        else:
            while run_system:
                ret, frame = cap.read()
                if not ret:
                    st.warning("Se perdió la señal de la cámara.")
                    break
                
                # El frame ya viene en BGR perfecto desde OpenCV. Lo enviamos directo.
                results = model_dist.predict(source=frame, conf=conf_threshold, imgsz=640, verbose=False)
                
                # plot() devuelve la imagen anotada en formato BGR
                annotated_frame = results[0].plot()
                
                # Streamlit necesita saber que los canales están en BGR
                FRAME_WINDOW.image(annotated_frame, channels="BGR")
                
            cap.release()

# ==========================================
# PESTAÑA 2: ANALIZAR IMÁGENES ESTÁTICAS
# ==========================================
with tab2:
    uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # SOLUCIÓN COLAB: Leer la imagen directamente con el motor de OpenCV en memoria (BGR)
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image_bgr = cv2.imdecode(file_bytes, 1) # 1 = cv2.IMREAD_COLOR (carga en BGR ignorando Alpha)

        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📸 Vista Entrada")
            # Mostramos la original pasándola temporalmente a RGB para la web
            st.image(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)
            
        with col2:
            st.markdown("### 👁️ Análisis de la IA")
            
            start_time = time.time()
            # Inferencia pura en BGR, idéntico a Colab
            results = model_dist.predict(source=image_bgr, conf=conf_threshold, imgsz=640, verbose=False)
            inference_duration = (time.time() - start_time) * 1000
            
            annotated_image = results[0].plot()
            st.image(annotated_image, channels="BGR", use_container_width=True)
            
        st.markdown("### 📊 Informe de Resultados")
        detecciones_totales = len(results[0].boxes)
        
        if detecciones_totales > 0:
            st.error(f"🚨 ALERTA: {detecciones_totales} detecciones en {inference_duration:.2f} ms")
            for box in results[0].boxes:
                cls_name = model_dist.names[int(box.cls[0])]
                st.markdown(f"• **Clase:** `{cls_name}` | **Confianza:** `{float(box.conf[0])*100:.2f}%`")
        else:
            st.success("✅ Conducción Segura detectada.")