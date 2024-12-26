# libs/orquestators/orquestador.py

from ui.logs import get_logger
from datetime import datetime
from controllers.file_controller import read_query_config
from libs.orquestators.quantio_items import process_file as process_items
from libs.orquestators.quantio_barcodes import process_file as process_barcodes
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas
from libs.barcode_selector import seleccionar_barcodes
from controllers.file_controller import save_processed_files, open_file, update_config_query
from tkinter import messagebox

# Obtener la función para actualizar logs
actualizar_log = get_logger()

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
        query_file_items = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], False)

        query_file_items_opt = None


        update_config_query('timestamp', fecha_actual)

        output_file = procesar_archivos(query_file_items, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        query_file_barcodes = process_barcodes()
        codebars_file = seleccionar_barcodes(output_file, query_file_barcodes)

        if items_file and codebars_file:
            res = save_processed_files(False)
            actualizar_log("Proceso completado")
        
        if config['optimizar_etiquetas'] == True:
            query_file_items_opt = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], config['optimizar_etiquetas'])
            output_file_opt = procesar_archivos(query_file_items_opt, file_path2)
            items_file_opt = calcular_ofertas(output_file_opt, file_propuesta)

            if items_file_opt:
                res = save_processed_files(True)
                actualizar_log("Proceso completado (optimizacion de etiquetas)")
        
        open_file(res)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        actualizar_log(f"Error: {str(e)}")
