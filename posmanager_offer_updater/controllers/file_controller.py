import os
import json
import csv
from datetime import datetime
from ui.logs import get_logger

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

def save_query_config(data):
    # Definir la ruta del directorio de salida
    output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\config')

    # Verificar si la carpeta existe; si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        actualizar_log(f"Directorio creado: {output_dir}")

    # Nombre del archivo de configuración
    archivo_configuracion = os.path.join(output_dir, "config_query_filters.json")

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