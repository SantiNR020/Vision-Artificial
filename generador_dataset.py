<<<<<<< HEAD
import os
import zipfile
import shutil
from PIL import Image

# Tus clases exactas (el orden es importante para mantener los IDs estables)
CLASSES = [
    "Drinking",
    "Hair and Makeup",
    "Operating Radio",
    "Reaching Behind",
    "Save Driving",
    "Talking Passenger",
    "Using Phone"
]

def crear_dataset_roboflow(zip_path, target_class, output_dir="roboflow_dataset"):
    if target_class not in CLASSES:
        print(f"❌ Error: La clase '{target_class}' no está en la lista de clases.")
        return

    class_id = CLASSES.index(target_class)
    
    # Crear estructura de carpetas
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")
    temp_dir = "temp_extracted"
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    print(f"📦 Extrayendo {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # El bounding box para toda la imagen en formato YOLO: class_id center_x center_y width height
    yolo_label_content = f"{class_id} 0.5 0.5 1.0 1.0\n"
    
    procesadas = 0
    # Recorrer los archivos extraídos
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                file_path = os.path.join(root, file)
                
                try:
                    # 1. Redimensionar la imagen a 432x432
                    img = Image.open(file_path)
                    img = img.convert('RGB') # Evitar problemas con canales alfa
                    img = img.resize((432, 432), Image.Resampling.LANCZOS)
                    
                    # 2. Guardar imagen en la carpeta final
                    base_name = os.path.splitext(file)[0]
                    new_img_name = f"{base_name}_{target_class.replace(' ', '')}.jpg"
                    img.save(os.path.join(images_dir, new_img_name), "JPEG", quality=95)
                    
                    # 3. Crear el archivo .txt de la etiqueta YOLO
                    label_path = os.path.join(labels_dir, f"{base_name}_{target_class.replace(' ', '')}.txt")
                    with open(label_path, 'w') as f:
                        f.write(yolo_label_content)
                        
                    procesadas += 1
                except Exception as e:
                    print(f"⚠️ Error procesando {file}: {e}")

    # Limpiar carpeta temporal
    shutil.rmtree(temp_dir)

    # 4. Generar el archivo data.yaml para Roboflow
    yaml_content = f"""train: images
val: images
nc: {len(CLASSES)}
names: {CLASSES}
"""
    with open(os.path.join(output_dir, "data.yaml"), 'w') as f:
        f.write(yaml_content)

    print(f"✅ ¡Completado! {procesadas} imágenes procesadas y etiquetadas como '{target_class}'.")
    print(f"📁 Tu dataset está listo en la carpeta: {output_dir}")

# ==========================================
# CONFIGURACIÓN DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # 1. Pon aquí el nombre de tu archivo ZIP
    ARCHIVO_ZIP = "fotos_bebiendo.zip" 
    
    # 2. Pon aquí la clase exacta a la que pertenecen las fotos del ZIP
    CLASE_A_ETIQUETAR = "Drinking"     
    
=======
import os
import zipfile
import shutil
from PIL import Image

# Tus clases exactas (el orden es importante para mantener los IDs estables)
CLASSES = [
    "Drinking",
    "Hair and Makeup",
    "Operating Radio",
    "Reaching Behind",
    "Save Driving",
    "Talking Passenger",
    "Using Phone"
]

def crear_dataset_roboflow(zip_path, target_class, output_dir="roboflow_dataset"):
    if target_class not in CLASSES:
        print(f"❌ Error: La clase '{target_class}' no está en la lista de clases.")
        return

    class_id = CLASSES.index(target_class)
    
    # Crear estructura de carpetas
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")
    temp_dir = "temp_extracted"
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    print(f"📦 Extrayendo {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # El bounding box para toda la imagen en formato YOLO: class_id center_x center_y width height
    yolo_label_content = f"{class_id} 0.5 0.5 1.0 1.0\n"
    
    procesadas = 0
    # Recorrer los archivos extraídos
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                file_path = os.path.join(root, file)
                
                try:
                    # 1. Redimensionar la imagen a 432x432
                    img = Image.open(file_path)
                    img = img.convert('RGB') # Evitar problemas con canales alfa
                    img = img.resize((432, 432), Image.Resampling.LANCZOS)
                    
                    # 2. Guardar imagen en la carpeta final
                    base_name = os.path.splitext(file)[0]
                    new_img_name = f"{base_name}_{target_class.replace(' ', '')}.jpg"
                    img.save(os.path.join(images_dir, new_img_name), "JPEG", quality=95)
                    
                    # 3. Crear el archivo .txt de la etiqueta YOLO
                    label_path = os.path.join(labels_dir, f"{base_name}_{target_class.replace(' ', '')}.txt")
                    with open(label_path, 'w') as f:
                        f.write(yolo_label_content)
                        
                    procesadas += 1
                except Exception as e:
                    print(f"⚠️ Error procesando {file}: {e}")

    # Limpiar carpeta temporal
    shutil.rmtree(temp_dir)

    # 4. Generar el archivo data.yaml para Roboflow
    yaml_content = f"""train: images
val: images
nc: {len(CLASSES)}
names: {CLASSES}
"""
    with open(os.path.join(output_dir, "data.yaml"), 'w') as f:
        f.write(yaml_content)

    print(f"✅ ¡Completado! {procesadas} imágenes procesadas y etiquetadas como '{target_class}'.")
    print(f"📁 Tu dataset está listo en la carpeta: {output_dir}")

# ==========================================
# CONFIGURACIÓN DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # 1. Pon aquí el nombre de tu archivo ZIP
    ARCHIVO_ZIP = "fotos_bebiendo.zip" 
    
    # 2. Pon aquí la clase exacta a la que pertenecen las fotos del ZIP
    CLASE_A_ETIQUETAR = "Drinking"     
    
>>>>>>> 956b5042b7c5b4e5bd97c2fc0e80abf1d41b91a0
    crear_dataset_roboflow(ARCHIVO_ZIP, CLASE_A_ETIQUETAR)