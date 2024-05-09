# Este script se ha realizado para unir subclases a nuevas clases, sustituyendo el valor por el dado {2:0}, 
# donde clase 2 pasa a ser 0, sin tocar la clase destino.
# Solo modifica los archivos .txt de anotaciones por lo que sólo hay que modificar labels_dir y class_mapping
#
# This script has been made to join subclasses to new classes, replacing the value with the given. f.e. {2:0},
# where class 2 becomes 0, without touching the target class.
# It only modifies the annotation .txt files, so you only have to modify labels_dir and class_mapping


import os

def apply_class_mapping(labels_dir, class_mapping):
    # Obtener la lista de archivos en el directorio de etiquetas
    label_files = [f for f in os.listdir(labels_dir) if os.path.isfile(os.path.join(labels_dir, f))]

    # Iterar sobre cada archivo de etiqueta
    for label_file in label_files:
        label_path = os.path.join(labels_dir, label_file)

        # Leer el contenido del archivo de etiqueta
        with open(label_path, 'r') as file:
            lines = file.readlines()

        # Modificar las clases según el mapeo proporcionado
        modified_lines = []
        for line in lines:
            # Separar la línea en partes (clase, coordenadas)
            parts = line.strip().split()
            if len(parts) > 0:
                class_id = int(parts[0])
                if class_id in class_mapping:
                    # Aplicar el mapeo de clases si la clase está en el mapeo
                    modified_class_id = class_mapping[class_id]
                    modified_line = f"{modified_class_id} {' '.join(parts[1:])}\n"
                    modified_lines.append(modified_line)
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)

        # Guardar los cambios en el archivo de etiqueta
        with open(label_path, 'w') as file:
            file.writelines(modified_lines)

if __name__ == "__main__":
    labels_dir = "./uniform/labels/val"
   # ejemplo de mapeo
    class_mapping = {1: 0, 2: 0}

    apply_class_mapping(labels_dir, class_mapping)