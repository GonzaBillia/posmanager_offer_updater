from controllers.query_controller import quantio_updated_products
from controllers.file_controller import guardar_resultados_como_csv
from ui.logs import get_logger

actualizar_log = get_logger()

file_path = "processed-files"
name = "items"

def process_file(day_filter):
    try:
        data = quantio_updated_products(day_filter)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        actualizar_log("El archivo Items Quantio se proceso correctamente")
        return output_file
    except Exception as e:
        actualizar_log(f"Ocurrio un Error en el proceso de la consulta: {e}")
        raise e

