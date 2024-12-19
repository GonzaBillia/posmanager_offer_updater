import tkinter as tk
from tkinter import ttk
from ui.logs import configurar_logger, get_logger

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Archivos para POSManager")

# Configurar el logger global
configurar_logger(root)

# Obtener la función para actualizar logs
actualizar_log = get_logger()

from ui.inputs import crear_inputs
from ui.buttons import crear_botones


# Agregar un mensaje inicial al log
actualizar_log("Aplicación iniciada")

# Crear los inputs y los botones desde los módulos correspondientes
entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars = crear_inputs(root)
crear_botones(root, entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars)

# Actualizar el log desde otro lugar
actualizar_log("Entradas creadas y botones configurados")

# Iniciar el bucle principal de la aplicación
root.mainloop()
