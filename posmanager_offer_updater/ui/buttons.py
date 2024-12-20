
from tkinter import ttk
from ui.logs import get_logger
from controllers.process_controller import process  # Importa la función desde el orquestador

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def procesar(entry_archivo2, entry_propuesta, entry_codebars):
    file_path2 = entry_archivo2.get()
    file_propuesta = entry_propuesta.get()
    file_codebars = entry_codebars.get()

    # Llamar al orquestador para procesar los archivos
    process(file_path2, file_propuesta, file_codebars)


def crear_botones(root, entry_archivo2, entry_propuesta, entry_codebars, db_connection_thread):
    # Botón para procesar
    button_procesar = ttk.Button(
        root, 
        text="Procesar Archivos", 
        command=lambda: procesar(entry_archivo2, entry_propuesta, entry_codebars)
    )
    button_procesar.grid(row=4, column=0, columnspan=3, pady=20, padx=10)

    return button_procesar
