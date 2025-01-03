from controllers.query_controller import quantio_updated_barcodes
from controllers.file_controller import guardar_resultados_como_csv

# Obtener el logger dinámicamente
def get_actualizar_log():
    from ui.logs import get_logger
    return get_logger()

file_path = "raw\\quantio\\barcodes"
name = "Barcodes"

def process_file(connection):
    try:
        data = quantio_updated_barcodes(connection)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        get_actualizar_log()("El archivo Barcodes Quantio se proceso correctamente")
        return output_file
    except Exception as e:
        get_actualizar_log()(f"Ocurrio un Error en el proceso de la consulta: {e}")
        raise e