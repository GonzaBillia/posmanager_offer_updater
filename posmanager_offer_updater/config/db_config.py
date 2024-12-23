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
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = None
        self.connection = None
        self.cursor = None

    def load_config(self):
        """Carga el archivo JSON con las credenciales de la base de datos."""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {self.config_path}")
            
            with open(self.config_path, "r") as file:
                self.config = json.load(file)
                # Validar las claves necesarias
                required_keys = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_DATABASE", "DB_PORT"]
                for key in required_keys:
                    if key not in self.config:
                        raise KeyError(f"Falta la clave {key} en el archivo de configuración.")
                actualizar_log("Archivo de configuración cargado correctamente.")
        except FileNotFoundError as e:
            messagebox.showerror("Error de configuración", f"No se encontró el archivo de configuración: {e}")
            actualizar_log(f"Error de configuración: {e}")
        except KeyError as e:
            messagebox.showerror("Error de configuración", f"Clave faltante en el archivo de configuración: {e}")
            actualizar_log(f"Clave faltante en el archivo de configuración: {e}")
        except json.JSONDecodeError as e:
            messagebox.showerror("Error de configuración", f"Error al leer el archivo JSON: {e}")
            actualizar_log(f"Error al leer el archivo JSON: {e}")

    def create_connection(self):
        """Crea y devuelve una conexión a la base de datos MySQL usando el archivo de configuración."""
        try:
            if self.config is None:
                self.load_config()  # Cargar configuración si no está cargada

            actualizar_log('Procesando configuración de conexión.')

            self.connection = pymysql.connect(
                host=self.config["DB_HOST"],
                user=self.config["DB_USER"],
                password=self.config["DB_PASSWORD"],
                database=self.config["DB_DATABASE"],
                port=int(self.config["DB_PORT"]),
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
