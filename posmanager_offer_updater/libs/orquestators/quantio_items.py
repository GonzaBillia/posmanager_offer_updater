from controllers.query_controller import quantio_updated_products, plex_updated_products, quantio_uexcluded_products
from controllers.file_controller import guardar_resultados_como_csv, excel_first_col_to_int_list
from ui.components.logs import get_logger
from config.db_onze_config import DBConfig

actualizar_log = get_logger()

db = DBConfig()
connection_pl = db.create_connection()

file_path = "raw\\quantio\\items"
name = "Items"

def process_file(day_filter, timestamp, is_timestamp, optimize_labels, connection):
    try:
        combined_data = quantio_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, connection)
        plex_data = plex_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, connection_pl)
        ean_list = excel_first_col_to_int_list()
        q_excluded = quantio_uexcluded_products(ean_list, connection)
        
        combined_data.extend(plex_data)
        combined_data.extend(q_excluded)
        
        # Eliminar duplicados usando IDProducto
        unique_data = {item["IDProducto"]: item for item in combined_data}

        output_file = guardar_resultados_como_csv(list(unique_data.values()), file_path, name)
        actualizar_log("El archivo Items Quantio se procesó correctamente")
        return output_file
    except Exception as e:
        actualizar_log(f"Ocurrió un Error en el proceso de la consulta: {e}")
        raise e


