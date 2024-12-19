import os
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
