import pymysql
import os
from ui.logs import get_logger
from config.db_config import DBConfig
from queries.quantio import cod1, cod2, Q_BARCODES, Q_UPDATED_PRODUCTS

actualizar_log = get_logger()

def quantio_updated_products(day_filter, timestamp, is_timestamp, optimize_labels):
    connection = None
    cursor = None
    try:
        # Obtener el directorio donde se encuentra el script actual (query_controller.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa al archivo config.json (supongamos que está en el directorio raíz o donde se llama)
        config_path = os.path.join(current_dir, '..', 'config.json')
        # Crear una nueva conexión a la base de datos
        db_config = DBConfig(config_path)  # Asegúrate de poner la ruta correcta al archivo de configuración
        connection = db_config.create_connection()  # Establece la conexión
        
        if connection:
            cursor = connection.cursor()
            actualizar_log("Cursor abierto para realizar consulta")

            # Ejecutar las sentencias SET sin usar multi=True
            cursor.execute(cod1)  # Ejecuta la primera sentencia SET
            cursor.execute(cod2)  # Ejecuta la segunda sentencia SET

            # Determinar el filtro a utilizar
            day_filter_value = timestamp if is_timestamp and timestamp is not None else day_filter

            optimize_labels_value = int(optimize_labels)  # True -> 1, False -> 0

            # Ejecutar la consulta con los parámetros adecuados
            cursor.execute(
                Q_UPDATED_PRODUCTS, 
                {"day_filter": day_filter_value, "optimize_labels": optimize_labels_value}
            )
            
            # Verificar si la consulta principal devuelve resultados
            resultados = cursor.fetchall()
            if resultados:  # Si hay resultados
                actualizar_log("Consulta realizada correctamente")
                return resultados
            else:
                actualizar_log("No hay resultados para la consulta.")
                return []
        else:
            actualizar_log("No se pudo establecer la conexión a la base de datos.")
            return []
        
    except pymysql.MySQLError as e:
        actualizar_log(f"Error ejecutando la consulta: {e}")
        return []
    
    finally:
        # Asegurarse de que el cursor y la conexión se cierren después de la consulta
        if cursor:
            cursor.close()
            actualizar_log("Cursor cerrado después de la consulta.")
        if connection:
            connection.close()  # Cerrar la conexión
            actualizar_log("Conexión cerrada.")

def quantio_updated_barcodes():
    connection = None
    cursor = None
    try:
        # Obtener el directorio donde se encuentra el script actual (query_controller.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa al archivo config.json (supongamos que está en el directorio raíz o donde se llama)
        config_path = os.path.join(current_dir, '..', 'config.json')
        # Crear una nueva conexión a la base de datos
        db_config = DBConfig(config_path)  # Asegúrate de poner la ruta correcta al archivo de configuración
        connection = db_config.create_connection()  # Establece la conexión
        
        if connection:
            cursor = connection.cursor()
            actualizar_log("Realizando consulta de códigos de barra a la base de datos")
            
            # Ejecutar la consulta SELECT
            cursor.execute(Q_BARCODES)

            # Verificar si la consulta principal devuelve resultados
            resultados = cursor.fetchall()
            if resultados:  # Si hay resultados
                actualizar_log("Consulta realizada correctamente")
                return resultados
            else:
                actualizar_log("No hay resultados para la consulta.")
                return []
        else:
            actualizar_log("No se pudo establecer la conexión a la base de datos.")
            return []
        
    except pymysql.MySQLError as e:
        actualizar_log(f"Error ejecutando la consulta: {e}")
        return []
    
    finally:
        # Asegurarse de que el cursor y la conexión se cierren después de la consulta
        if cursor:
            cursor.close()
        if connection:
            connection.close()  # Cerrar la conexión
            actualizar_log("Conexión cerrada.")
