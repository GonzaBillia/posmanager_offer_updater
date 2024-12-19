import tkinter as tk
from tkinter import messagebox
from ui.logs import get_logger
from libs.update_normalizer import procesar_archivos
from libs.offer_calculator import calcular_ofertas
from libs.barcode_selector import seleccionar_barcodes

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def procesar(entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars):
    file_path1 = entry_archivo1.get()
    file_path2 = entry_archivo2.get()
    file_propuesta = entry_propuesta.get()
    file_codebars = entry_codebars.get()

    if not file_path1 or not file_path2 or not file_propuesta or not file_codebars:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        actualizar_log("Seleccione el / los archivos faltantes.")
        return

    try:
        output_file = procesar_archivos(file_path1, file_path2)
        items_file = calcular_ofertas(output_file, file_propuesta)
        codebars_file = seleccionar_barcodes(output_file, file_codebars)
        
        if items_file and codebars_file:
            messagebox.showinfo("Éxito", f"El archivo de resultados y los codigos de barra han sido guardados exitosamente")
            actualizar_log("Proceso completado")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        actualizar_log("Error: ")


def crear_botones(root, entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars, db_connection_thread):
    # Botón para procesar
    button_procesar = tk.Button(
        root, 
        text="Procesar Archivos", 
        command=lambda: procesar(entry_archivo1, entry_archivo2, entry_propuesta, entry_codebars)
    )
    button_procesar.grid(row=4, column=0, columnspan=1, pady=20, padx=10)

    # Botón para recargar la configuración y probar la conexión
    reload_button = tk.Button(
        root, 
        text="Recargar", 
        command=db_connection_thread  # Asignar la función recargada
    )
    reload_button.grid(row=4, column=1, pady=20, padx=10)

    return button_procesar, reload_button

# Función para desactivar el botón de recarga
def desactivar_boton_recarga(reload_button):
    reload_button.config(state=tk.DISABLED)  # Desactivar el botón

# Función para activar el botón de recarga
def activar_boton_recarga(reload_button):
    reload_button.config(state=tk.NORMAL)  # Reactivar el botón

