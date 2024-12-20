import tkinter as tk
import os
import time
import threading
from tkinter import messagebox
from ui.logs import configurar_logger, get_logger

# CONFIGURACION INICIAL DE LA VENTANA

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Archivos para POSManager")

# Configurar el logger global y Obtener la función para actualizar logs
configurar_logger(root)
actualizar_log = get_logger()

# CONFIGURACION INICIAL DE LA VENTANA



# CONFIGURACION INICIAL DE DB Y ELEMENTOS UI

# imports posteriores a la configuracion
from ui.inputs import crear_inputs
from ui.buttons import crear_botones, desactivar_boton_recarga, activar_boton_recarga
from config.db_config import DBConfig

# Obtener el directorio del script actual (donde está main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al archivo config.json
config_path = os.path.join(current_dir, 'config.json')

# Crear la instancia de DBConfig usando la ruta correcta
db_config = DBConfig(config_path)

# Variable global para controlar el estado de la conexión
conexion_en_proceso = False

# Función para intentar conectar a la base de datos
def connect_to_db():
    
    global conexion_en_proceso
    conexion_en_proceso = True
    # Desactivar el botón de recarga mientras se conecta
    root.after(0, lambda: desactivar_boton_recarga(reload_button))
    connection = db_config.create_connection()
    
    if connection:
        connection.close()

    # Reactivar el botón de recarga después de intentar la conexión
    conexion_en_proceso = False
    root.after(0, lambda: activar_boton_recarga(reload_button))

# Función para manejar la conexión en un hilo separado
def db_connection_thread():
    actualizar_log("Conectando a la base de datos...")
    connect_to_db()


# Función para manejar el cierre de la ventana
def on_closing():
    respuesta = messagebox.askquestion("Confirmar cierre", "¿Estás seguro de que deseas cerrar la ventana?")
    
    if respuesta == 'yes':
        # Cerrar la conexión de la base de datos
        # Cerrar la conexión de la base de datos aquí
        actualizar_log("Finalizando Procesos")
        db_config.close_connection()
        actualizar_log("Conexion a base de datos cerrada")
        root.destroy()  # Cerrar la ventana y terminar el programa

# Configurar la ventana para que ejecute on_closing al cerrarla
root.protocol("WM_DELETE_WINDOW", on_closing)


# Crear los inputs y los botones desde los módulos correspondientes
entry_archivo2, entry_propuesta, entry_codebars = crear_inputs(root)
button_procesar, reload_button = crear_botones(root, entry_archivo2, entry_propuesta, entry_codebars, db_connection_thread)

# CONFIGURACION INICIAL DE DB Y ELEMENTOS UI



# INICIALIZACION DE LA APLICACION E HILOS

# Agregar un mensaje inicial al log
actualizar_log("Aplicación iniciada")

# Iniciar el hilo para la conexión a la base de datos
threading.Thread(target=db_connection_thread, daemon=True).start()

# Iniciar el bucle principal de la aplicación
root.mainloop()

# INICIALIZACION DE LA APLICACION E HILOS