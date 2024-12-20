import json
import mysql.connector
from mysql.connector import Error
from ui.logs import get_logger
import os


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
                database=self.config["DB_DATABASE"],
                port=self.config["DB_PORT"]
            )

            if self.connection.is_connected():
                actualizar_log("Conexión exitosa!")
                return self.connection
        except (Error, FileNotFoundError, ValueError, KeyError) as e:
            actualizar_log(f"Ha ocurrido un error en la conexion: {e}")
            actualizar_log("Comprueba tu configuración.")
            return None

    def check_connection(self):
        """Verifica si la conexión está activa."""
        try:
            if self.connection and self.connection.is_connected():
                return True
            else:
                actualizar_log("Conexión no activa. Reconectando")
                self.create_connection()  # Reintenta conectar
                return self.connection and self.connection.is_connected()
        except Error as e:
            actualizar_log(f"Error al verificar la conexión: {e}")
            return False

    def close_connection(self):
        if self.connection:
            self.connection.close()
    
    def open_cursor(self):
        if self.check_connection():
            try:
                self.cursor = self.connection.cursor(dictionary=True)
                actualizar_log("cursor abierto para realizar consulta")
                return self.cursor
            except Error as e:
                actualizar_log(f"Ocurrio un error al querer abrir el cursor {e}")
                raise e
        else:
            actualizar_log("La conexión no está activa. No se pudo abrir el cursor.")
            raise ConnectionError("No se pudo abrir el cursor porque la conexión no está activa.")
    

