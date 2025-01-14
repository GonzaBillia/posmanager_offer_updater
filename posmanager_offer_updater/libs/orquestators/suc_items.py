from config.db_onze_config import DBConfig
from controllers.query_controller import plex_suc_stock
from controllers.file_controller import save_file_as_csv
from ui.components.logs import get_logger
import pandas as pd

actualizar_log = get_logger()

db = DBConfig()
connection = db.create_connection()

file_path = "raw\\plex\\items"
name = "Items"

def filter_by_suc(file):
    try:
        df = pd.read_csv(file, delimiter=';', on_bad_lines='skip')


        dfp = plex_suc_stock(connection)
        
        # Convierte a DataFrame si es una lista
        if isinstance(dfp, list):
            dfp = pd.DataFrame(dfp)

        # Verifica si el DataFrame tiene la columna 'IDProducto'
        if 'IDProducto' not in dfp.columns:
            raise ValueError("El DataFrame no contiene la columna 'IDProducto'.")

        df_filtered = pd.merge(df, dfp[['IDProducto']], how='inner', on='IDProducto')

        output = save_file_as_csv(df_filtered, file_path, name)

        actualizar_log("El archivo Items filtrado Plex se procesó correctamente")
        
        return output
    except Exception as e:
        actualizar_log(f"Ocurrió un Error en el proceso de la consulta: {e}")
        raise e