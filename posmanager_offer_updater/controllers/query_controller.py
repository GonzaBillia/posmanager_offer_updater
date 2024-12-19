import mysql.connector
from ui.logs import get_logger
from config.db_config import DBConfig as db
from queries.quantio import cod1, cod2, Q_PRODUCTS

actualizar_log = get_logger()

def quantio_updated_products(day_filter):
    try:
        cursor = db.open_cursor()
        
        # Ejecutar las declaraciones SET
        cursor.execute(cod1)
        cursor.execute(cod2)
        
        # Ejecutar la consulta principal con el parámetro `cantidad_dias`
        cursor.execute(Q_PRODUCTS, {"day_filter": day_filter})
        
        # Obtener los resultados
        resultados = cursor.fetchall()

        actualizar_log("Se realizo la consulta a la base de datos correctamente")
        
        return resultados
    except mysql.connector.Error as e:
        actualizar_log(f"Error ejecutando la consulta: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
            actualizar_log("Cursor cerrado después de la consulta.")