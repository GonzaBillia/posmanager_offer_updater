import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ui.logs import get_logger
from ui.windows import ventana_query_quantio

# Obtener la función para actualizar logs
actualizar_log = get_logger()

# def seleccionar_archivo_entrada1(output_file):
#     # file_path = filedialog.askopenfilename(title="Seleccionar la consulta de la Base de Datos", filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])
#     # if file_path:
#     #     entry_archivo1.delete(0, tk.END)
#     #     entry_archivo1.insert(0, file_path)
#     #     actualizar_log(f"Archivo de base de datos seleccionado: {file_path}")
#     # Asignar la ruta del archivo output_file al entry
#     entry_archivo1.delete(0, tk.END)  # Limpiar el campo actual
#     entry_archivo1.insert(0, output_file) 

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

def crear_inputs(root):
    # Inputs y botones para los archivos
    label_archivo1 = ttk.Label(root, text="Seleccionar la consulta de la Base de Datos (CSV delimitado por punto y coma):")
    label_archivo1.grid(row=0, column=0, padx=10, pady=10)

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


    label_codebars = ttk.Label(root, text="Seleccionar Query de Codigos de Barras (CSV delimitado por punto y coma):")
    label_codebars.grid(row=3, column=0, padx=10, pady=10)

    entry_codebars = ttk.Entry(root, width=50)
    entry_codebars.grid(row=3, column=1, padx=10, pady=10)

    button_codebars = ttk.Button(root, text="Buscar", command=lambda: seleccionar_archivo_codebars(entry_codebars))
    button_codebars.grid(row=3, column=2, padx=10, pady=10)


    return entry_archivo2, entry_propuesta, entry_codebars
