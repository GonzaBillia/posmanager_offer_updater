import os
import sys
import subprocess
import datetime
import shutil
import json
import csv
import pandas as pd
from datetime import datetime
from ui.components.logs import get_logger

actualizar_log = get_logger()

def guardar_resultados_como_csv(results,final_path,name):
    """
    Guarda los resultados de una consulta en un archivo CSV dentro de la carpeta de salida predefinida.

    Args:
        resultados (list[dict]): Lista de resultados (deben ser diccionarios).
    """
    if not results:
        actualizar_log("No hay resultados para guardar.")
        return

    # Definir la ruta del directorio de salida (misma ruta que usas para otros archivos)
    output_dir = os.path.expanduser(f'~\\Documents\\PM-offer-updater\\{final_path}')

    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        actualizar_log(f"Directorio creado: {output_dir}")

    # Crear el nombre de archivo con la fecha de hoy
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f"{name}-{fecha_hoy}.csv")

    # Obtener los encabezados del primer resultado
    encabezados = results[0].keys()

    try:
        # Guardar los resultados en el archivo CSV
        with open(output_file, mode='w', encoding='utf-8', newline='') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=encabezados, delimiter=';')
            
            # Escribir encabezados
            writer.writeheader()
            
            # Escribir filas
            writer.writerows(results)
        
        actualizar_log(f"Resultados guardados exitosamente en {output_file}.")

        return output_file
    except Exception as e:
        actualizar_log(f"Error al guardar resultados en CSV: {e}")
        raise e

def save_direct_file(data, name):
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    if not data:
        actualizar_log("No hay resultados para guardar.")
        return

    # Convertir los datos en un DataFrame si es necesario
    if isinstance(data, list):  # Si los datos son una lista
        try:
            data = pd.DataFrame(data)  # Convertir a DataFrame
        except ValueError as e:
            actualizar_log(f"Error al convertir los datos a DataFrame: {e}")
            return

    # Definir la ruta del directorio de salida (misma ruta que usas para otros archivos)
    output_dir = os.path.expanduser(f'~\\Documents\\PM-offer-updater\\processed-files\\Results\\{fecha_hoy}')

    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        actualizar_log(f"Directorio creado: {output_dir}")

    # Crear el nombre de archivo con la fecha de hoy
    output_file = os.path.join(output_dir, f"{name}.txt")

    data.to_csv(output_file, sep='\t', index=False, header=False)

    return output_file

import os
import shutil
from datetime import datetime

def save_proposal_backup(input_file):
    # Crear la ruta de salida
    output_dir = os.path.expanduser(f'~\\Documents\\PM-offer-updater\\processed-files\\History\\Propuesta')

    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Crear el nombre del archivo de salida
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f"Propuesta.xlsx")

    # Copiar el archivo de entrada a la ruta de salida
    try:
        shutil.copy(input_file, output_file)
        actualizar_log(f"Copia de seguridad creada: {output_file}")
        return output_file
    except Exception as e:
        actualizar_log(f"Error al crear la copia de seguridad: {e}")
        return None


def save_query_config(data):
    # Definir la ruta del directorio de salida
    output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\config')

    # Verificar si la carpeta existe; si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        actualizar_log(f"Directorio creado: {output_dir}")

    # Nombre del archivo de configuración
    archivo_configuracion = os.path.join(output_dir, "config_query_filters.json")

    # Asegurarse de que los datos son válidos para JSON
    if not isinstance(data, dict):
        raise ValueError("Los datos a guardar deben ser un diccionario válido.")
    
    # Guardar la configuración en el archivo
    with open(archivo_configuracion, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Imprimir y registrar en el log
    actualizar_log(f"Configuración guardada en: {archivo_configuracion}")

def read_query_config():
    # Definir la ruta del directorio de configuración
    configuraciones_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\config')
    archivo_configuracion = os.path.join(configuraciones_dir, "config_query_filters.json")

    # Verificar si el archivo existe
    if not os.path.exists(archivo_configuracion):
        actualizar_log(f"El archivo de configuración no existe: {archivo_configuracion}")
        return None

    try:
        # Leer el archivo JSON
        with open(archivo_configuracion, 'r') as json_file:
            configuracion = json.load(json_file)
        
        actualizar_log(f"Configuración cargada desde: {archivo_configuracion}")
        return configuracion

    except Exception as e:
        actualizar_log(f"Error al leer el archivo de configuración: {str(e)}")
        return None
    
def update_config_query(key, value):
    """
    Actualiza un campo específico en el archivo de configuración JSON.

    Parámetros:
        key: La clave del campo que se desea actualizar.
        value: El nuevo valor para el campo especificado.
    """
    # Leer la configuración actual
    configuracion = read_query_config()

    # Actualizar el campo especificado
    configuracion[key] = value

    # Guardar los cambios
    save_query_config(configuracion)

    # Log de la operación
    actualizar_log(f"Configuración actualizada: {key} = {value}")


def save_processed_files(isOpt):
    # Definir la fecha de hoy
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')

    # Definir las rutas de los directorios de origen
    output_dir_codebars = os.path.expanduser('~\\Documents\\PM-offer-updater\\processed-files\\Codebars')
    output_dir_items = os.path.expanduser('~\\Documents\\PM-offer-updater\\processed-files\\calculated-items')

    # Definir la ruta de destino en Results
    file_path = os.path.expanduser(f'~\\Documents\\PM-offer-updater\\processed-files\\Results\\{fecha_hoy}')

    # Crear la carpeta Results si no existe
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # Función para buscar y copiar el archivo a la carpeta de destino
    def copiar_archivo(archivo_origen, destino, nuevo_nombre):
        if os.path.exists(archivo_origen):
            # Copiar archivo al destino con el nuevo nombre
            shutil.copy(archivo_origen, os.path.join(destino, nuevo_nombre))
            actualizar_log(f"Archivo copiado: {nuevo_nombre} a {destino}")
        else:
            actualizar_log(f"Archivo no encontrado: {archivo_origen}")

    # Lógica para copiar archivos según el valor de isOpt
    if isOpt:
        # Buscar y copiar el archivo `Items`
        items_file = os.path.join(output_dir_items, f"calc-items-opt-{fecha_hoy}.txt")
        copiar_archivo(items_file, file_path, "Items-opt.txt")
    else:
        # Buscar y copiar el archivo `Items`
        items_file = os.path.join(output_dir_items, f"calc-items-{fecha_hoy}.txt")
        copiar_archivo(items_file, file_path, "Items.txt")

        # Buscar y copiar el archivo `Codebars`
        codebars_file = os.path.join(output_dir_codebars, f"CodBarras-{fecha_hoy}.txt")
        copiar_archivo(codebars_file, file_path, "CodBarras.txt")

    # Lógica para dividir los archivos en partes de 5000 filas si superan ese límite
    def dividir_archivo_en_partes(ruta_archivo, filas_por_archivo=5000):
        if os.path.exists(ruta_archivo):
            try:
                # Leer con manejo de líneas problemáticas y columnas variables
                df = pd.read_csv(
                    ruta_archivo,
                    sep='\t',
                    encoding='utf-16',
                    engine='python',
                    on_bad_lines='warn',  # Ignorar líneas malas
                    names=[f"col_{i}" for i in range(36)],  # Ajusta al número esperado de columnas
                    header=None
                )

                # Dividir solo si supera el límite de filas
                if len(df) > filas_por_archivo:
                    for i in range(0, len(df), filas_por_archivo):
                        sub_df = df.iloc[i:i + filas_por_archivo]
                        parte_numero = i // filas_por_archivo + 1
                        nombre_sub_archivo = os.path.join(
                            os.path.dirname(ruta_archivo),
                            f"{os.path.basename(ruta_archivo).split('.')[0]}_parte_{parte_numero}.txt"
                        )

                        # Exportar con formato adecuado
                        sub_df.to_csv(
                            nombre_sub_archivo,
                            sep='\t',
                            encoding='utf-16',
                            index=False,
                            header=False  # Sin encabezado si no existía en el archivo original
                        )
                        print(f"Archivo dividido generado: {nombre_sub_archivo}")
                else:
                    print(f"El archivo {ruta_archivo} no supera las {filas_por_archivo} filas. No se dividió.")
            except Exception as e:
                print(f"Error al procesar el archivo {ruta_archivo}: {e}")

    # Aplicar la división a los archivos copiados
    if isOpt:
        dividir_archivo_en_partes(os.path.join(file_path, "Items-opt.txt"))
    else:
        dividir_archivo_en_partes(os.path.join(file_path, "Items.txt"))
        dividir_archivo_en_partes(os.path.join(file_path, "CodBarras.txt"))

    # Registro de la acción final
    actualizar_log("Archivos copiados y divididos correctamente en la carpeta Results.")

    return file_path


def open_file(file_path):
    if os.path.exists(file_path):
        # Intentar abrir la carpeta con el explorador de archivos
        if os.name == 'nt':  # Para sistemas Windows
            subprocess.run(['explorer', file_path])
        elif os.name == 'posix':  # Para sistemas Unix/Linux/Mac
            subprocess.run(['open', file_path])
        actualizar_log(f"Carpeta con resultados abierta: {file_path}")
    else:
        actualizar_log("La carpeta de resultados no existe.")

def get_resource_path(relative_path):
    """Obtiene la ruta absoluta del archivo, ya sea en desarrollo o en un .exe."""
    if hasattr(sys, '_MEIPASS'):
        # Si se está ejecutando desde un .exe, usa el directorio temporal.
        base_path = sys._MEIPASS
    else:
        # En desarrollo, usa el directorio del script.
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)