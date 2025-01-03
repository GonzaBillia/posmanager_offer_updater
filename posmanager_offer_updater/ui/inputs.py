import tkinter as tk
import os
from tkinter import ttk
from tkinter import filedialog
from ui.logs import get_logger
from ui.windows import ventana_query_quantio, config

# Obtener la función para actualizar logs
actualizar_log = get_logger()
re_etiqueta_var = tk.BooleanVar(value=False)

def seleccionar_archivo_entrada2(entry_archivo2):
    file_path = filedialog.askopenfilename(title="Seleccionar la lista de Items de POSManager", filetypes=[("Archivos TXT", "*.txt"), ("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])
    if file_path:
        entry_archivo2.delete(0, tk.END)
        entry_archivo2.insert(0, file_path)
        actualizar_log(f"Lista de Items de POSManager seleccionada: {file_path}")

def seleccionar_archivo_propuesta(entry_propuesta):
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de Propuesta", filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
    if file_path:
        entry_propuesta.delete(0, tk.END)
        entry_propuesta.insert(0, file_path)
        actualizar_log(f"Archivo de Propuesta seleccionado: {file_path}")

def seleccionar_archivo_codebars(entry_codebars):
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de código de barras", filetypes=[("Archivos CSV", "*.csv"),("Archivos Excel", "*.xlsx;*.xls")])
    if file_path:
        entry_codebars.delete(0, tk.END)
        entry_codebars.insert(0, file_path)
        actualizar_log(f"Archivo de código de barras seleccionado: {file_path}")

def revisar_var_etiqueta():
    return re_etiqueta_var.get()

def crear_inputs(root):
    default_propuesta = os.path.expanduser('~\\Documents\\PM-offer-updater\\import\\Propuesta.xlsx')
    # Inputs y botones para los archivos
    label_archivo1 = ttk.Label(root, text="Items actualizados recientemente (Consulta a la base de datos):")
    label_archivo1.grid(row=0, column=0, padx=10, pady=10)

    # label2_archivo1 = ttk.Label(root, text=f"Cantidad de dias contemplados: {config['dias']}")
    # label2_archivo1.grid(row=0, column=1, padx=10, pady=10)

    button_query = ttk.Button(root, text="Filtro", command=lambda: ventana_query_quantio(root))
    button_query.grid(row=0, column=2, padx=10, pady=10)


    label_archivo2 = ttk.Label(root, text="Seleccionar la lista de Items de POSManager (TXT delimitado por comas):")
    label_archivo2.grid(row=1, column=0, padx=10, pady=10)

    entry_archivo2 = ttk.Entry(root, width=50)
    entry_archivo2.grid(row=1, column=1, padx=10, pady=10)

    button_archivo2 = ttk.Button(root, text="Buscar", command=lambda: seleccionar_archivo_entrada2(entry_archivo2))
    button_archivo2.grid(row=1, column=2, padx=10, pady=10)


    label_propuesta = ttk.Label(root, text="Seleccionar archivo de Propuesta (Excel):")
    label_propuesta.grid(row=2, column=0, padx=10, pady=10)

    entry_propuesta = ttk.Entry(root, width=50)
    entry_propuesta.grid(row=2, column=1, padx=10, pady=10)

    button_propuesta = ttk.Button(root, text="Buscar", command=lambda: seleccionar_archivo_propuesta(entry_propuesta))
    button_propuesta.grid(row=2, column=2, padx=10, pady=10)

    # Crear el Checkbutton asociado a la variable de control
    re_etiqueta_check = tk.Checkbutton(root, text="Primer Re Etiquetado Mensual", variable=re_etiqueta_var)
    re_etiqueta_check.grid(row=3, column=1, padx=10, pady=10)

    entry_propuesta.insert(0, default_propuesta)

    return entry_archivo2, entry_propuesta, re_etiqueta_var.get()
