import tkinter as tk
import os
from tkinter import ttk
from ui.logs import configurar_logger, get_logger

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Archivos para POSManager")

# Configurar el logger global y Obtener la función para actualizar logs
configurar_logger(root)
actualizar_log = get_logger()

# imports posteriores a la configuracion
from ui.inputs import crear_inputs
from ui.buttons import crear_botones
from config.db_config import DBConfig

# Obtener el directorio del script actual (donde está main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al archivo config.json
config_path = os.path.join(current_dir, 'config.json')

# Crear la instancia de DBConfig usando la ruta correcta
db_config = DBConfig(config_path)


# Función para intentar conectar a la base de datos
def connect_to_db():
    connection = db_config.create_connection()
    if connection:
        actualizar_log("Conexión exitosa a la base de datos.")
    else:
        actualizar_log("Conexión fallida. Esperando cambios en la configuración.")

# Función para recargar la configuración y probar la conexión nuevamente
def reload_db_config():
    db_config.reload_config()  # Recargar la configuración
    connect_to_db()  # Intentar nuevamente la conexión

# Crear los inputs y los botones desde los módulos correspondientes
entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars = crear_inputs(root)
crear_botones(root, entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars, reload_db_config)

# Intentar conectar a la base de datos al iniciar
connect_to_db()

# Iniciar el bucle principal de la aplicación
root.mainloop()

# Agregar un mensaje inicial al log
actualizar_log("Aplicación iniciada")
