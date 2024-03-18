# Este script se ha realizado para normalizar el tamaño un dataset con anotaciones en formato yolo
# (clase, x, y, width, height) a un tamaño cuadrado específico (640) manteniendo la
# relación de aspecto de la imagen añadiendo padding gris a ambos lados de la dimensión faltante.
# 
#This script has been made to normalize the size of a dataset with annotations in yolo format 
#(class, x, y, width, height) to a specific square size (640) maintaining the aspect ratio
# of the image by adding gray padding to both sides of the missing dimension.
#


import os
import cv2
import numpy as np

# Funcion para redimensionar una imagen manteniendo su aspecto
# Function to resize an image while maintaining its appearance

def resize_image(image_path, target_size):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    if height > width:
        scale = target_size / height
        new_width = int(width * scale)
        resized_img = cv2.resize(img, (new_width, target_size))
        left_padding = (target_size - new_width) // 2
        right_padding = target_size - new_width - left_padding
        resized_img = cv2.copyMakeBorder(resized_img, 0, 0, left_padding, right_padding, cv2.BORDER_CONSTANT, value=(140, 140, 140))
        padding = (left_padding / target_size, 0)
    else:
        scale = target_size / width
        new_height = int(height * scale)
        resized_img = cv2.resize(img, (target_size, new_height))
        top_padding = (target_size - new_height) // 2
        bottom_padding = target_size - new_height - top_padding
        resized_img = cv2.copyMakeBorder(resized_img, top_padding, bottom_padding, 0, 0, cv2.BORDER_CONSTANT, value=(140, 140, 140))
        padding = (0, top_padding / target_size)
    return resized_img, scale, padding, img.shape

# Funcion para ajustar las coordenadas de los bounding boxes para el nuevo tamaño y relleno
# Function to adjust the coordinates of the bounding boxes for the new size and padding
def resize_boxes(boxes, scale, padding, original_size):
    padded_x, padded_y = padding
    resized_boxes = []
    for box in boxes:
        c, x, y, w, h = box
        if padded_x > 0:
            w = w * scale * original_size[1]/target_size
            x = (x * original_size[1] / original_size[0]) + padded_x
        elif padded_y > 0:
            h = h * scale * original_size[0]/target_size
            y = (y * original_size[0] / original_size[1]) + padded_y
        # Si no hay padding, las coordenadas se mantienen
        # If there is no padding, the coordinates are kept    
        resized_boxes.append((int(c), x, y, w, h))
    return resized_boxes


# Directorio del dataset, imágenes y etiquetas
# Directory of the dataset, images and labels
dataset_dir = './dataset'
images_dir = os.path.join(dataset_dir, 'images')
labels_dir = os.path.join(dataset_dir, 'labels')

# Nuevo tamaño deseado
# New desired size
target_size = 640

# Iterar sobre las imagenes y etiquetas
# Iterate over images and tags
for image_name in os.listdir(images_dir):
    image_path = os.path.join(images_dir, image_name)
    if os.path.isfile(image_path):
        # Redimensionar la imagen
        resized_img, scale, padding, original_size = resize_image(image_path, target_size)
        
        # Leer las etiquetas
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_name)
        
        if os.path.isfile(label_path):
            with open(label_path, 'r') as f:
                boxes = []
                for line in f.readlines():
                    box = [float(x) for x in line.strip().split()]
                    boxes.append(box)
            # Redimensionar las coordenadas de los bounding boxes
            resized_boxes = resize_boxes(boxes, scale, padding, original_size)
            
            # Guardar la imagen redimensionada
            cv2.imwrite(image_path, resized_img)
            
            # Guardar las nuevas etiquetas
            with open(label_path, 'w') as f:
                for box in resized_boxes:
                    f.write(' '.join([str(coord) for coord in box]) + '\n')
        else:
            print(f"No se encontro la etiqueta correspondiente para {image_name}")
