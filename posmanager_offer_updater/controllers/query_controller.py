import pymysql
import os
from ui.logs import get_logger
from queries.quantio import cod1, cod2, Q_BARCODES, Q_UPDATED_PRODUCTS, Q_DEPARTMENTS, Q_FAMILIES, Q_PROVIDERS

actualizar_log = get_logger()

def quantio_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, connection):
    cursor = None
    try:        
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
                Q_UPDATED_PRODUCTS
                
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

def quantio_updated_barcodes(connection):
    cursor = None
    try:

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

def quantio_updated_departments(connection):
    cursor = None
    try:

        if connection:
            cursor = connection.cursor()
            actualizar_log("Realizando consulta de departamentos a la base de datos")
            
            # Ejecutar la consulta SELECT
            cursor.execute(Q_DEPARTMENTS)

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

def quantio_updated_families(connection):
    cursor = None
    try:

        if connection:
            cursor = connection.cursor()
            actualizar_log("Realizando consulta de familias a la base de datos")
            
            # Ejecutar la consulta SELECT
            cursor.execute(Q_FAMILIES)

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

def quantio_updated_providers(connection):
    cursor = None
    try:

        if connection:
            cursor = connection.cursor()
            actualizar_log("Realizando consulta de familias a la base de datos")
            
            # Ejecutar la consulta SELECT
            cursor.execute(Q_PROVIDERS)

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