# libs/orquestators/orquestador.py
import os
from ui.logs import get_logger
from datetime import datetime
from config.db_config import DBConfig
from controllers.file_controller import read_query_config
from libs.orquestators.quantio_items import process_file as process_items
from libs.orquestators.quantio_barcodes import process_file as process_barcodes
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas, optimizar_lectoras
from libs.barcode_selector import seleccionar_barcodes
from controllers.file_controller import save_processed_files, open_file, update_config_query
from tkinter import messagebox

# Obtener la función para actualizar logs
actualizar_log = get_logger()

# Obtener el directorio donde se encuentra el script actual (query_controller.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ruta completa al archivo config.json (supongamos que está en el directorio raíz o donde se llama)
config_path = os.path.join(current_dir, '..', 'config.json')

db_config = DBConfig(config_path)  # Asegúrate de poner la ruta correcta al archivo de configuración

def process(file_path2, file_propuesta):
    if not file_path2 or not file_propuesta:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        actualizar_log("Seleccione el / los archivos faltantes.")
        return
    
    config = read_query_config()

    fecha_actual = datetime.now()

    fecha_actual = datetime.strftime(fecha_actual, '%Y-%m-%d %H-%M-%S')

    # Inicializar el valor de 'timestamp' si no existe
    if 'optimizar_etiquetas' not in config:
        config['optimizar_etiquetas'] = False

    if 'usar_timestamp' not in config:
        config['usar_timestamp'] = False
        
    timestamp_actual = config.get('timestamp', None)

    try:
        connection = db_config.create_connection()

        query_file_items = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], False, connection)

        query_file_items_opt = None


        update_config_query('timestamp', fecha_actual)

        output_file = procesar_archivos(query_file_items, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        query_file_barcodes = process_barcodes(connection)
        codebars_file = seleccionar_barcodes(output_file, query_file_barcodes)

        if items_file and codebars_file:
            res = save_processed_files(False)
            actualizar_log("Proceso completado")
        
        if config['optimizar_etiquetas'] == True:
            query_file_items_opt = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], config['optimizar_etiquetas'], connection)
            output_file_opt = procesar_archivos(query_file_items_opt, file_path2)
            is_Items, items_file_opt = calcular_ofertas(output_file_opt, file_propuesta)

            # Cambio de precios para lectoras:
            is_opt = optimizar_lectoras(items_file_opt)


            if is_Items and is_opt:
                res = save_processed_files(True)
                actualizar_log("Proceso completado (optimizacion de etiquetas)")
        
        open_file(res)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        actualizar_log(f"Error: {str(e)}")

    finally:
        if connection:
            connection.close()  # Cerrar la conexión
            actualizar_log("Conexión cerrada.")
