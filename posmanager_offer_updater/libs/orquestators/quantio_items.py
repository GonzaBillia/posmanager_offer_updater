from controllers.query_controller import quantio_updated_products, plex_updated_products
from controllers.file_controller import guardar_resultados_como_csv
from ui.components.logs import get_logger
from config.db_onze_config import DBConfig

actualizar_log = get_logger()

db = DBConfig()
connection_pl = db.create_connection()

file_path = "raw\\quantio\\items"
name = "Items"

def process_file(day_filter, timestamp, is_timestamp, optimize_labels, connection):
    try:
        data = quantio_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, connection)
        plex_data = plex_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, connection_pl)
        data.extend(plex_data)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        actualizar_log("El archivo Items Quantio se proceso correctamente")
        return output_file
    except Exception as e:
        actualizar_log(f"Ocurrio un Error en el proceso de la consulta: {e}")
        raise e

