import tkinter as tk
from tkinter import ttk
from ui.inputs import crear_inputs
from ui.buttons import crear_botones
from ui.logs import configurar_logs


# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Archivos para POSManager")

# Configurar los logs
log_area, actualizar_log = configurar_logs(root)

# Crear los inputs y los botones desde los módulos correspondientes
entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars = crear_inputs(root)
crear_botones(root, entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars)

# Iniciar el bucle principal de la aplicación
root.mainloop()
