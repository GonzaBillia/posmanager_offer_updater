import tkinter as tk
from tkinter import messagebox
from ui.logs import configurar_logger, get_logger
from config.env import init_env

# CONFIGURACION INICIAL DE LA VENTANA

init_env()

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Archivos para POSManager")

# Configurar el logger global y obtener la función para actualizar logs
try:
    configurar_logger(root)
    actualizar_log = get_logger()
except RuntimeError as e:
    print(f"Error: {e}")
    actualizar_log = print  # Reemplazo temporal para evitar fallos críticos


# CONFIGURACION INICIAL DE LA VENTANA



# CONFIGURACION INICIAL DE DB Y ELEMENTOS UI

# imports posteriores a la configuracion
from ui.inputs import crear_inputs
from ui.buttons import crear_botones

# Función para manejar el cierre de la ventana
def on_closing():
    respuesta = messagebox.askquestion("Confirmar cierre", "¿Estás seguro de que deseas cerrar la ventana?")
    
    if respuesta == 'yes':
        # Cerrar la conexión de la base de datos
        # Cerrar la conexión de la base de datos aquí
        actualizar_log("Finalizando Procesos")
        root.destroy()  # Cerrar la ventana y terminar el programa

# Configurar la ventana para que ejecute on_closing al cerrarla
root.protocol("WM_DELETE_WINDOW", on_closing)

# Crear los inputs y los botones desde los módulos correspondientes
entry_archivo2, entry_propuesta = crear_inputs(root)
button_procesar = crear_botones(root, entry_archivo2, entry_propuesta)

# CONFIGURACION INICIAL DE DB Y ELEMENTOS UI



# INICIALIZACION DE LA APLICACION E HILOS

# Agregar un mensaje inicial al log
actualizar_log("Aplicación iniciada")

# Iniciar el bucle principal de la aplicación
root.mainloop()

# INICIALIZACION DE LA APLICACION E HILOS