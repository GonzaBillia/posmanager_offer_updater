from controllers.query_controller import quantio_updated_barcodes
from controllers.file_controller import guardar_resultados_como_csv
from ui.components.logs import get_logger

actualizar_log = get_logger()

file_path = "raw\\quantio\\barcodes"
name = "Barcodes"

def process_file(connection):
    try:
        data = quantio_updated_barcodes(connection)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        actualizar_log("El archivo Barcodes Quantio se proceso correctamente")
        return output_file
    except Exception as e:
        actualizar_log(f"Ocurrio un Error en el proceso de la consulta: {e}")
        raise e

