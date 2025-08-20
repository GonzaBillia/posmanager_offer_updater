import pymysql
import os
from typing import List, Tuple
from ui.components.logs import get_logger
from queries.quantio import cod1, cod2, Q_BARCODES, Q_UPDATED_PRODUCTS, Q_DEPARTMENTS, Q_FAMILIES, Q_PROVIDERS, Q_SELECTED_PRODUCTS, Q_EXCLUDED_PRODUCTS
from queries.plex import P_STOCK, P_PRODUCTS, P_BARCODES
from datetime import datetime, date

actualizar_log = get_logger()


def format_date_for_mysql(value):
    if isinstance(value, str):
        # Probar con varios formatos
        for fmt in ('%Y-%m-%d', '%Y-%m-%d %H-%M-%S', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y'):
            try:
                dt = datetime.strptime(value, fmt)
                # Si tiene hora, devolvé el datetime completo. Si no, solo la fecha.
                if 'H' in fmt:
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        raise ValueError(f"El valor '{value}' no es un formato de fecha soportado (debe ser YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, DD/MM/YYYY).")
    elif isinstance(value, (datetime, date)):
        # Si el objeto tiene hora distinta de 00:00:00, incluí la hora
        if isinstance(value, datetime) and (value.hour != 0 or value.minute != 0 or value.second != 0):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return value.strftime('%Y-%m-%d')
    else:
        raise ValueError(f"El valor '{value}' no es tipo fecha ni string válido.")


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
            
def quantio_uexcluded_products(id_list: List[int], connection):
    cursor = None
    try:
        if not id_list:
            actualizar_log("La lista de IDs está vacía.")
            return []

        cursor = connection.cursor()
        actualizar_log("Cursor abierto para realizar consulta")

        # Ejecutar las sentencias SET (cod1, cod2)
        cursor.execute(cod1)
        cursor.execute(cod2)

        # Generamos un marcador %s por cada elemento en la lista
        placeholders = ", ".join(["%s"] * len(id_list))
        sql = Q_EXCLUDED_PRODUCTS.format(placeholders=placeholders)

        # Ejecutamos pasando la lista como parámetros posicionales
        cursor.execute(sql, tuple(id_list))

        resultados = cursor.fetchall()
        if resultados:
            actualizar_log("Consulta realizada correctamente")
            return resultados
        else:
            actualizar_log("No hay resultados para la consulta.")
            return []

    except pymysql.MySQLError as e:
        actualizar_log(f"Error ejecutando la consulta: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
            actualizar_log("Cursor cerrado después de la consulta.")

def quantio_selected_products(list, connection):
    cursor = None
    try:        
        if connection:
            cursor = connection.cursor()
            actualizar_log("Cursor abierto para realizar consulta")

            # Ejecutar las sentencias SET sin usar multi=True
            cursor.execute(cod1)  # Ejecuta la primera sentencia SET
            cursor.execute(cod2)  # Ejecuta la segunda sentencia SET

            
            # Ejecutar la consulta con los parámetros adecuados
            cursor.execute(
                Q_SELECTED_PRODUCTS,
                {"list": list}
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

def plex_updated_barcodes(connection):
    cursor = None
    try:

        if connection:
            cursor = connection.cursor()
            actualizar_log("Realizando consulta de códigos de barra a la base de datos")
            
            # Ejecutar la consulta SELECT
            cursor.execute(P_BARCODES)

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

def plex_suc_stock(connection):
    cursor = None
    try:

        if connection:
            cursor = connection.cursor()
            actualizar_log("Realizando consulta de Items de sucursal a la base de datos")
            
            # Ejecutar la consulta SELECT
            cursor.execute(P_STOCK)

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

def plex_updated_products(day_filter, timestamp, is_timestamp, optimize_labels, connection):
    cursor = None
    try:        
        if connection:
            cursor = connection.cursor()
            actualizar_log("Cursor abierto para realizar consulta")

            # Determinar el filtro a utilizar
            day_filter_value = timestamp if is_timestamp and timestamp is not None else day_filter
            day_filter_value = format_date_for_mysql(day_filter_value)
            optimize_labels_value = int(optimize_labels)  # True -> 1, False -> 0
            # Ejecutar la consulta con los parámetros adecuados
            cursor.execute(
                P_PRODUCTS,
                {"day_filter": day_filter_value}
            )
            
            # Verificar si la consulta principal devuelve resultados
            resultados = cursor.fetchall()
            if resultados:  # Si hay resultados
                actualizar_log("Consulta realizada correctamente")
                for row in resultados:
                    # row es un diccionario
                    if 'm.FechaUltimoPrecio' in row:
                        row['FechaUltimoPrecio'] = row.pop('m.FechaUltimoPrecio')
                    if '.FechaUltimoPrecio' in row:
                        row['FechaUltimoPrecio'] = row.pop('.FechaUltimoPrecio')
                    if 'm.idTipoIVA' in row:
                        row['idTipoIVA'] = row.pop('m.idTipoIVA')
                    
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
