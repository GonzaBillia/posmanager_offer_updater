# libs/orquestators/orquestador.py

from ui.logs import get_logger
from controllers.file_controller import read_query_config
from libs.orquestators.quantio_items import process_file as process_items
from libs.orquestators.quantio_barcodes import process_file as process_barcodes
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas
from libs.barcode_selector import seleccionar_barcodes
from controllers.file_controller import save_processed_files, open_file
from tkinter import messagebox

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def process(file_path2, file_propuesta):
    if not file_path2 or not file_propuesta:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        actualizar_log("Seleccione el / los archivos faltantes.")
        return
    
    config = read_query_config()

    try:
        query_file_items = process_items(config['dias'])
        output_file = procesar_archivos(query_file_items, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        query_file_barcodes = process_barcodes()
        codebars_file = seleccionar_barcodes(output_file, query_file_barcodes)
        
        if items_file and codebars_file:
            res = save_processed_files()
            actualizar_log("Proceso completado")
            open_file(res)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        actualizar_log(f"Error: {str(e)}")
