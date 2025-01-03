from controllers.query_controller import quantio_updated_products
from controllers.file_controller import guardar_resultados_como_csv

def get_actualizar_log():
    from ui.logs import get_logger
    return get_logger()

file_path = "raw\\quantio\\items"
name = "Items"

def process_file(day_filter, timestamp, is_timestamp, optimize_labels, re_etiqueta_var, connection):
    try:
        data = quantio_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, re_etiqueta_var, connection)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        get_actualizar_log()("El archivo Items Quantio se proceso correctamente")
        return output_file
    except Exception as e:
        get_actualizar_log()(f"Ocurrio un Error en el proceso de la consulta: {e}")
        raise e

