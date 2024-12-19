import json
import mysql.connector
from mysql.connector import Error
from ui.logs import get_logger
import os
import time

# Obtener la función para actualizar logs
actualizar_log = get_logger()

class DBConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = None
        self.connection = None

    def load_config(self):
        """Carga el archivo JSON con las credenciales de la base de datos."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {self.config_path}")
        
        with open(self.config_path, "r") as file:
            try:
                self.config = json.load(file)
                # Validar las claves necesarias
                required_keys = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_DATABASE"]
                for key in required_keys:
                    if key not in self.config:
                        raise KeyError(f"Falta la clave {key} en el archivo de configuración.")
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al leer el archivo de configuración: {e}")

    def create_connection(self):
        """Crea y devuelve una conexión a la base de datos MySQL usando el archivo de configuración."""
        try:
            if self.config is None:
                self.load_config()  # Cargar configuración si no está cargada

            self.connection = mysql.connector.connect(
                host=self.config["DB_HOST"],
                user=self.config["DB_USER"],
                password=self.config["DB_PASSWORD"],
                database=self.config["DB_DATABASE"]
            )

            if self.connection.is_connected():
                actualizar_log("Conexión a la base de datos exitosa.")
                return self.connection
        except (Error, FileNotFoundError, ValueError, KeyError) as e:
            actualizar_log(f"Error al conectar a la base de datos: {e}")
            return None

    def wait_for_config_change(self):
        """Espera a que el archivo de configuración sea modificado y recarga la configuración."""
        actualizar_log("Esperando cambios en el archivo de configuración...")
        while True:
            try:
                # Esperar 5 segundos entre cada intento de recarga
                time.sleep(5)
                self.load_config()
                actualizar_log("Archivo de configuración recargado.")
                return
            except Exception as e:
                actualizar_log(f"Error al cargar configuración: {e}")
                actualizar_log("Esperando nuevo intento...")

    def reload_config(self):
        """Recargar la configuración y probar la conexión nuevamente."""
        self.connection = self.create_connection()
        if self.connection:
            actualizar_log("Conexión exitosa tras recargar configuración.")
        else:
            actualizar_log("No se pudo conectar, esperando cambios en el archivo de configuración.")
            self.wait_for_config_change()
