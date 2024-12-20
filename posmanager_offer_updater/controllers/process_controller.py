# libs/orquestators/orquestador.py

from ui.logs import get_logger
from controllers.file_controller import read_query_config
from libs.orquestators.quantio_items import process_file
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas
from libs.barcode_selector import seleccionar_barcodes
from controllers.file_controller import save_processed_files
from tkinter import messagebox

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def process(file_path2, file_propuesta, file_codebars):
    if not file_path2 or not file_propuesta or not file_codebars:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        actualizar_log("Seleccione el / los archivos faltantes.")
        return
    
    config = read_query_config()

    try:
        query_file = process_file(config['dias'])
        output_file = procesar_archivos(query_file, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        codebars_file = seleccionar_barcodes(output_file, file_codebars)
        
        if items_file and codebars_file:
            save_processed_files()
            actualizar_log("Proceso completado")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        actualizar_log(f"Error: {str(e)}")
