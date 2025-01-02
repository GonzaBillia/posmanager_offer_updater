
from tkinter import ttk
from ui.logs import get_logger
from ui.inputs import revisar_var_etiqueta
from controllers.process_controller import process  # Importa la función desde el orquestador

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def procesar(entry_archivo2, entry_propuesta, re_etiqueta_var):
    file_path2 = entry_archivo2.get()
    file_propuesta = entry_propuesta.get()
    re_etiqueta_var = revisar_var_etiqueta()
    # Llamar al orquestador para procesar los archivos
    process(file_path2, file_propuesta, re_etiqueta_var)


def crear_botones(root, entry_archivo2, entry_propuesta, re_etiqueta_var):
    # Botón para procesar
    button_procesar = ttk.Button(
        root, 
        text="Procesar Archivos", 
        command=lambda: procesar(entry_archivo2, entry_propuesta, re_etiqueta_var)
    )
    button_procesar.grid(row=4, column=0, columnspan=3, pady=20, padx=10)

    return button_procesar
