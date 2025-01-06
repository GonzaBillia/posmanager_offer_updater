import json
import pymysql
from pymysql import MySQLError
from tkinter import messagebox
from ui.components.logs import get_logger
import os
import logging

# Configura los logs de depuración
logging.basicConfig(level=logging.DEBUG)

# Obtener la función para actualizar logs
actualizar_log = get_logger()

class DBConfig:
    @staticmethod
    def create_connection():
        """Crea y devuelve una conexión a la base de datos MySQL usando el archivo de configuración."""
        try:
            actualizar_log('Procesando configuración de conexión.')

            connection = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE"),
                port=int(os.getenv("DB_PORT")),
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8'
            )

            actualizar_log('Conexión abierta, comprobando...')

            if connection:
                actualizar_log("Conexión exitosa!")
                return connection
        except (MySQLError, FileNotFoundError, ValueError, KeyError) as e:
            messagebox.showerror("Error de conexión", f"Ha ocurrido un error en la conexión: {e}")
            actualizar_log(f"Ha ocurrido un error en la conexión: {e}")
            return None

    @staticmethod
    def check_connection(connection):
        """Verifica si la conexión está activa."""
        try:
            if connection and connection.open:
                return True
            else:
                actualizar_log("Conexión no activa.")
                return False
        except MySQLError as e:
            messagebox.showerror("Error de conexión", f"Error al verificar la conexión: {e}")
            actualizar_log(f"Error al verificar la conexión: {e}")
            return False

    @staticmethod
    def close_connection(connection):
        """Cierra la conexión a la base de datos si está activa."""
        try:
            if connection and connection.open:
                connection.close()
                actualizar_log("Conexión cerrada correctamente.")
            else:
                actualizar_log("No hay conexión activa para cerrar.")
        except MySQLError as e:
            messagebox.showerror("Error al cerrar conexión", f"Error al intentar cerrar la conexión: {e}")
            actualizar_log(f"Error al cerrar conexión: {e}")

    @staticmethod
    def open_cursor(connection):
        """Abre un cursor para realizar consultas."""
        try:
            if DBConfig.check_connection(connection):
                cursor = connection.cursor()
                actualizar_log("Cursor abierto para realizar consulta.")
                return cursor
            else:
                messagebox.showerror("Error de conexión", "No se pudo abrir el cursor porque la conexión no está activa.")
                raise ConnectionError("No se pudo abrir el cursor porque la conexión no está activa.")
        except MySQLError as e:
            messagebox.showerror("Error al abrir cursor", f"Ocurrió un error al abrir el cursor: {e}")
            actualizar_log(f"Ocurrió un error al abrir el cursor: {e}")
            raise e
