import json
import pymysql
from pymysql import MySQLError
from tkinter import messagebox
from ui.logs import get_logger
import os
import logging

# Configura los logs de depuración
logging.basicConfig(level=logging.DEBUG)

# Obtener la función para actualizar logs
actualizar_log = get_logger()

class DBConfig:
    def __init__(self):
        self.config = None
        self.connection = None
        self.cursor = None

    def create_connection(self):
        """Crea y devuelve una conexión a la base de datos MySQL usando el archivo de configuración."""
        try:
            actualizar_log('Procesando configuración de conexión.')

            self.connection = pymysql.connect(
                host=os.getenv["DB_HOST"],
                user=os.getenv["DB_USER"],
                password=os.getenv["DB_PASSWORD"],
                database=os.getenv["DB_DATABASE"],
                port=int(os.getenv["DB_PORT"]),
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8'
            )

            actualizar_log('Conexión abierta, comprobando...')

            if self.connection:
                actualizar_log("Conexión exitosa!")
                return self.connection
        except (MySQLError, FileNotFoundError, ValueError, KeyError) as e:
            messagebox.showerror("Error de conexión", f"Ha ocurrido un error en la conexión: {e}")
            actualizar_log(f"Ha ocurrido un error en la conexión: {e}")
            return None

    def check_connection(self):
        """Verifica si la conexión está activa."""
        try:
            if self.connection:
                return True
            else:
                actualizar_log("Conexión no activa. Intentando reconectar...")
                self.create_connection()  # Reintenta conectar
                if self.connection:
                    actualizar_log("Reconexión exitosa.")
                    return True
                else:
                    messagebox.showerror("Error de conexión", "No se pudo restablecer la conexión a la base de datos.")
                    return False
        except MySQLError as e:
            messagebox.showerror("Error de conexión", f"Error al verificar la conexión: {e}")
            actualizar_log(f"Error al verificar la conexión: {e}")
            return False

    def close_connection(self):
        """Cierra la conexión a la base de datos si está activa."""
        try:
            if self.connection:
                self.connection.close()
                actualizar_log("Conexión cerrada correctamente.")
            else:
                actualizar_log("No hay conexión activa para cerrar.")
        except MySQLError as e:
            messagebox.showerror("Error al cerrar conexión", f"Error al intentar cerrar la conexión: {e}")
            actualizar_log(f"Error al cerrar conexión: {e}")

    def open_cursor(self):
        """Abre un cursor para realizar consultas."""
        try:
            if self.check_connection():
                self.cursor = self.connection.cursor()
                actualizar_log("Cursor abierto para realizar consulta.")
                return self.cursor
            else:
                messagebox.showerror("Error de conexión", "No se pudo abrir el cursor porque la conexión no está activa.")
                raise ConnectionError("No se pudo abrir el cursor porque la conexión no está activa.")
        except MySQLError as e:
            messagebox.showerror("Error al abrir cursor", f"Ocurrió un error al abrir el cursor: {e}")
            actualizar_log(f"Ocurrió un error al abrir el cursor: {e}")
            raise e
