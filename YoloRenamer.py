# Este script se ha realizado para normalizar el nombre de los archivos de un dataset
# de imagenes y etiquetas .txt. Acepta que haya imagenes sin label.
# 
# This script has been made to normalize the name of the files of a dataset 
# of images and labels .txt
#

import os
import shutil

def rename_images_and_labels(images_dir, labels_dir, nombreraiz):
    # Obtener la lista de archivos en los directorios de imagenes y etiquetas
    image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    label_files = [f for f in os.listdir(labels_dir) if os.path.isfile(os.path.join(labels_dir, f))]
    
    # Ordenar archivos para garantizar consistencia en la numeracion
    image_files.sort()
    
    # Renombrar archivos
    for i, image_file in enumerate(image_files):
        # Verificar si existe una etiqueta correspondiente
        label_file = image_file.split('.')[0] + '.txt'
        
        # Obtener la extension del archivo de imagen original
        image_ext = os.path.splitext(image_file)[1]
        
        # Construir el nuevo nombre de archivo
        new_name = f"{nombreraiz}_{i:05d}"  # Modificar :05d si se desean poner diferentes digitos
        
        # Renombrar archivo de imagen
        old_image_path = os.path.join(images_dir, image_file)
        new_image_path = os.path.join(images_dir, f"{new_name}{image_ext}")
        os.rename(old_image_path, new_image_path)
        
        # Renombrar archivo de etiqueta si existe
        if label_file in label_files:
            old_label_path = os.path.join(labels_dir, label_file)
            new_label_path = os.path.join(labels_dir, f"{new_name}.txt")
            os.rename(old_label_path, new_label_path)
        else:
            print(f"No se encuentra una etiqueta correspondiente para {image_file}, ahora llamado {new_name}{image_ext}.")

if __name__ == "__main__":
    images_dir = "./uniform/images/val"
    labels_dir = "./uniform/labels/val"
    nombreraiz = "uni_val3"

    rename_images_and_labels(images_dir, labels_dir, nombreraiz)
