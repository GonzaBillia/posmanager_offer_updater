import tkinter as tk
from tkinter import messagebox
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas
from libs.barcode_selector import seleccionar_barcodes

def procesar(entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars):
    file_path1 = entry_archivo1.get()
    file_path2 = entry_archivo2.get()
    file_propuesta = entry_propuesta.get()
    file_codebars = entry_codebars.get()

    if not file_path1 or not file_path2 or not file_propuesta:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        return

    try:
        output_file = procesar_archivos(file_path1, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        codebars_file = seleccionar_barcodes(output_file, file_codebars)
        
        if items_file:
            messagebox.showinfo("Éxito", f"El archivo de resultados ha sido guardado exitosamente")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def crear_botones(root, entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars, log_area):
    # Botón para procesar
    button_procesar = tk.Button(root, text="Procesar Archivos", command=lambda: procesar(entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars, log_area))
    button_procesar.grid(row=4, column=0, columnspan=3, pady=20)
