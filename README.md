# Detección de Distracciones al Volante (YOLOv8)

Este proyecto desarrolla un sistema de visión artificial en tiempo real capaz de detectar comportamientos de riesgo en conductores (uso de móvil, distracciones, etc.) utilizando una arquitectura **YOLOv8 Nano**.

##  Resumen del Proyecto
El objetivo principal es la seguridad vial mediante la monitorización proactiva del habitáculo. A través de un **Estudio de Ablación** riguroso, hemos optimizado un modelo de red neuronal para que sea capaz de ejecutarse en tiempo real en hardware de bajos recursos (*Edge Computing*), manteniendo una alta precisión en la detección de distracciones.

##  Metodología: Estudio de Ablación
Hemos comparado 6 configuraciones distintas para entender cómo afectan los hiperparámetros al rendimiento del modelo:

- **Modelo Base:** YOLOv8n (Configuración estándar).
- **V1 (Sin Mosaico):** Optimización de la geometría espacial del habitáculo.
- **V2 (AdamW):** Prueba de optimizador adaptativo (fallida).
- **V3 (Rotación 15°):** Mejora de robustez ante baches y desalineación de cámara.
- **V4 (Alta Resolución):** Captura de micro-gestos mediante entrada de 800px.
- **V5 (Dropout 0.15):** Freno de memorización para forzar la generalización.

##  Resultados Principales
El modelo logró una precisión sobresaliente en el entorno de validación, aunque detectamos un *overfitting* estadístico debido a la estructura de los datos de origen.

| Experimento | Época Óptima | mAP50-95 (%) | Box Loss |
| :--- | :--- | :--- | :--- |
| Modelo Base | 25 | 98.70 | 0.0932 |
| V5 (Dropout) | 25 | 98.70 | 0.0932 |
| V4 (Alta Res) | 29 | 98.41 | 0.1651 |
| V1 (Sin Mosaico) | 30 | 98.27 | 0.0728 |
| V3 (Rotación) | 30 | 98.16 | 0.0873 |
| V2 (AdamW) | 20 | 18.34 | 0.1337 |

##  Validación Empírica
Más allá de las métricas de laboratorio, hemos desarrollado un prototipo funcional en **Streamlit**. 
- **Hallazgo clave:** Se ha diagnosticado un *Domain Shift* (cambio de dominio). El modelo funciona de forma excelente con imágenes que comparten características ópticas con el entrenamiento, pero requiere *Domain Adaptation* para cámaras web frontales de baja calidad.

##  Roadmap de Desarrollo
Para llevar el prototipo a producción, estamos trabajando en:
1. **Pseudo-etiquetado:** Uso de la IA actual como anotador automático para escalar el dataset.
2. **Data Augmentation Destructivo:** Simulación de ruido y mala calidad de cámara para forzar la robustez.
3. **Validación Externa:** Aislamiento de conductores en los datasets de entrenamiento y validación para eliminar la fuga de datos.

##  Stack Tecnológico
- **IA:** [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- **Interfaz:** [Streamlit](https://streamlit.io/)
- **Entorno:** Google Colab
- **Post-procesado:** Python, Pandas, OpenCV

---
*Proyecto desarrollado como estudio de investigación aplicada en Visión Artificial.*
