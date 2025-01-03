import os
from datetime import datetime
from config.db_config import DBConfig
from controllers.file_controller import read_query_config
from libs.orquestators.quantio_items import process_file as process_items
from libs.orquestators.quantio_barcodes import process_file as process_barcodes
from libs.orquestators.quantio_categories import process_categories_files as process_categories
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas, optimizar_lectoras
from libs.barcode_selector import seleccionar_barcodes
from controllers.file_controller import save_processed_files, open_file, update_config_query
from tkinter import messagebox

# Obtener el logger dinámicamente
def get_actualizar_log():
    from ui.logs import get_logger
    return get_logger()

def process(file_path2, file_propuesta, re_etiqueta_var):
    if not file_path2 or not file_propuesta:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        get_actualizar_log()("Seleccione el / los archivos faltantes.")
        return
    
    config = read_query_config()
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    # Inicializar valores de configuración si no existen
    config.setdefault('optimizar_etiquetas', False)
    config.setdefault('usar_timestamp', False)
    config.setdefault('dpts_fams', False)
    
    timestamp_actual = config.get('timestamp', None)

    try:
        connection = DBConfig.create_connection()
        get_actualizar_log()('Conexión abierta, comprobando...')

        query_file_items = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], False, re_etiqueta_var, connection)
        update_config_query('timestamp', fecha_actual)

        output_file = procesar_archivos(query_file_items, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        query_file_barcodes = process_barcodes(connection)
        codebars_file = seleccionar_barcodes(output_file, query_file_barcodes)

        if items_file and codebars_file:
            res = save_processed_files(False)
            get_actualizar_log()("Proceso completado")

        if config['optimizar_etiquetas']:
            query_file_items_opt = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], config['optimizar_etiquetas'], re_etiqueta_var, connection)
            output_file_opt = procesar_archivos(query_file_items_opt, file_path2)
            is_Items, items_file_opt = calcular_ofertas(output_file_opt, file_propuesta)

            is_opt = optimizar_lectoras(items_file_opt)
            if is_Items and is_opt:
                res = save_processed_files(True)
                get_actualizar_log()("Proceso completado (optimización de etiquetas)")

        if config['dpts_fams']:
            process_categories(connection)
            get_actualizar_log()("Proceso completado (obtención de categorías)")

        open_file(res)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        get_actualizar_log()(f"Error: {str(e)}")

    finally:
        if connection:
            connection.close()
            get_actualizar_log()("Conexión cerrada.")
