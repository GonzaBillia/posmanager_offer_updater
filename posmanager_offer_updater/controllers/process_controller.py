# libs/orquestators/orquestador.py
import os
from ui.components.logs import get_logger
from datetime import datetime
from config.db_config import DBConfig
from controllers.file_controller import read_query_config, save_proposal_backup
from libs.orquestators.quantio_items import process_file as process_items
from libs.orquestators.quantio_barcodes import process_file as process_barcodes
from libs.orquestators.quantio_categories import process_categories_files as process_categories
from libs.orquestators.proposal_items import process_proposal
from libs.orquestators.suc_items import filter_by_suc
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas, optimizar_lectoras
from libs.barcode_selector import seleccionar_barcodes
from controllers.file_controller import save_processed_files, open_file, update_config_query
from tkinter import messagebox


# Obtener la función para actualizar logs
actualizar_log = get_logger()



def process(file_path2, file_propuesta, option, hilo_progreso):
    if not file_path2 or not file_propuesta:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        actualizar_log("Seleccione el / los archivos faltantes.")
        return
    
    config = read_query_config()

    fecha_actual = datetime.now()

    fecha_actual = datetime.strftime(fecha_actual, '%Y-%m-%d %H-%M-%S')
    hilo_progreso.progreso_actualizado.emit(100 // 16)

    # Inicializar el valor de 'timestamp' si no existe

    if 'usar_timestamp' not in config:
        config['usar_timestamp'] = False

    if 'dpts_fams' not in config:
        config['dpts_fams'] = False
        
    timestamp_actual = config.get('timestamp', None)

    try:
        connection = DBConfig.create_connection()
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 2)

        if option != 0:
            price_changes = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], False, connection)
            query_file_items = process_proposal(file_propuesta, option, price_changes, connection)
        else:
            query_file_items = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], False, connection)

        hilo_progreso.progreso_actualizado.emit(100 // 16 * 3)

        query_file_items_opt = None

        update_config_query('timestamp', fecha_actual)

        output_file = procesar_archivos(query_file_items, file_path2)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 4)
        is_items, items_file = calcular_ofertas(output_file, file_propuesta)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 5)
        query_file_barcodes = process_barcodes(connection)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 6)
        codebars_file = seleccionar_barcodes(output_file, query_file_barcodes)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 7)

        is_opt = optimizar_lectoras(items_file, True)

        if is_opt and codebars_file:
            res = save_processed_files(False)
            hilo_progreso.progreso_actualizado.emit(100 // 16 * 8)
            actualizar_log("Proceso completado")
        

        # Optimizacion de Etiquetas
        if option != 0:
            price_changes = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], True, connection)
            query_file_items_all = process_proposal(file_propuesta, option, price_changes, connection)
            query_file_items_opt = filter_by_suc(query_file_items_all)

        else:    
            query_file_items_all = process_items(config['dias'], timestamp_actual, config['usar_timestamp'], True, connection)
            query_file_items_opt = filter_by_suc(query_file_items_all)
        
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 9)
        output_file_opt = procesar_archivos(query_file_items_opt, file_path2)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 10)
        is_Items, items_file_opt = calcular_ofertas(output_file_opt, file_propuesta)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 11)

        # Cambio de precios para lectoras:
        is_opt = optimizar_lectoras(items_file_opt, False)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 12)


        if is_Items and is_opt:
            res = save_processed_files(True)
            hilo_progreso.progreso_actualizado.emit(100 // 16 * 13)
            actualizar_log("Proceso completado (optimizacion de etiquetas)")
        
        if config['dpts_fams'] == True:
            process_categories(connection)
            hilo_progreso.progreso_actualizado.emit(100 // 16 * 14)
            actualizar_log("Proceso completado (obtencion de categorias)")

        open_file(res)
        hilo_progreso.progreso_actualizado.emit(100 // 16 * 15)
        
        save_proposal_backup(file_propuesta)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        actualizar_log(f"Error: {str(e)}")

    finally:
        if connection:
            connection.close()  # Cerrar la conexión
            hilo_progreso.progreso_actualizado.emit(100)
            actualizar_log("Conexión cerrada.")
            hilo_progreso.detener()
