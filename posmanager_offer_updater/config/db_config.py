import json
import pymysql
from pymysql import MySQLError
from tkinter import messagebox
import os
import logging

# Configura los logs de depuración
logging.basicConfig(level=logging.DEBUG)

def get_actualizar_log():
    from ui.logs import get_logger
    return get_logger()

class DBConfig:
    @staticmethod
    def create_connection():
        """Crea y devuelve una conexión a la base de datos MySQL usando el archivo de configuración."""
        try:
            get_actualizar_log()('Procesando configuración de conexión.')

            connection = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE"),
                port=int(os.getenv("DB_PORT")),
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8'
            )

            get_actualizar_log()('Conexión abierta, comprobando...')

            if connection:
                get_actualizar_log()("Conexión exitosa!")
                return connection
        except (MySQLError, FileNotFoundError, ValueError, KeyError) as e:
            messagebox.showerror("Error de conexión", f"Ha ocurrido un error en la conexión: {e}")
            get_actualizar_log()(f"Ha ocurrido un error en la conexión: {e}")
            return None
