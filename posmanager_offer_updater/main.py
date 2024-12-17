import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from libs.update_normalizer import procesar_archivos  # Importamos la función del procesamiento
from libs.offer_calculator import calcular_ofertas #Importamos la funcion del calculo de ofertas

def seleccionar_archivo_entrada1():
    file_path = filedialog.askopenfilename(title="Seleccionar la consulta de la Base de Datos", filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])
    entry_archivo1.delete(0, tk.END)  # Limpiar la entrada antes de poner el nuevo texto
    entry_archivo1.insert(0, file_path)

def seleccionar_archivo_entrada2():
    file_path = filedialog.askopenfilename(title="Seleccionar la lista de Items de POSManager", filetypes=[("Archivos TXT", "*.txt"), ("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])
    entry_archivo2.delete(0, tk.END)
    entry_archivo2.insert(0, file_path)

def seleccionar_archivo_propuesta():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de Propuesta", filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
    entry_propuesta.delete(0, tk.END)
    entry_propuesta.insert(0, file_path)

def procesar():
    file_path1 = entry_archivo1.get()
    file_path2 = entry_archivo2.get()
    file_propuesta = entry_propuesta.get()

    if not file_path1 or not file_path2 or not file_propuesta:
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los archivos antes de continuar.")
        return

    try:
        output_file = procesar_archivos(file_path1, file_path2, file_propuesta)  # Pasar el nuevo parámetro al procesador
        items_file = calcular_ofertas(output_file, file_propuesta)
        messagebox.showinfo("Éxito", f"El archivo de resultados ha sido guardado exitosamente")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Archivos para POSManager")

# Crear una etiqueta y caja de texto para seleccionar el primer archivo
label_archivo1 = ttk.Label(root, text="Seleccionar la consulta de la Base de Datos (CSV delimitado por tabulaciones):")
label_archivo1.grid(row=0, column=0, padx=10, pady=10)

entry_archivo1 = ttk.Entry(root, width=50)
entry_archivo1.grid(row=0, column=1, padx=10, pady=10)

button_archivo1 = ttk.Button(root, text="Buscar", command=seleccionar_archivo_entrada1)
button_archivo1.grid(row=0, column=2, padx=10, pady=10)

# Crear una etiqueta y caja de texto para seleccionar el segundo archivo
label_archivo2 = ttk.Label(root, text="Seleccionar la lista de Items de POSManager (TXT delimitado por comas):")
label_archivo2.grid(row=1, column=0, padx=10, pady=10)

entry_archivo2 = ttk.Entry(root, width=50)
entry_archivo2.grid(row=1, column=1, padx=10, pady=10)

button_archivo2 = ttk.Button(root, text="Buscar", command=seleccionar_archivo_entrada2)
button_archivo2.grid(row=1, column=2, padx=10, pady=10)

# Crear una etiqueta y caja de texto para seleccionar el archivo de propuesta
label_propuesta = ttk.Label(root, text="Seleccionar archivo de Propuesta (Excel):")
label_propuesta.grid(row=2, column=0, padx=10, pady=10)

entry_propuesta = ttk.Entry(root, width=50)
entry_propuesta.grid(row=2, column=1, padx=10, pady=10)

button_propuesta = ttk.Button(root, text="Buscar", command=seleccionar_archivo_propuesta)
button_propuesta.grid(row=2, column=2, padx=10, pady=10)

# Botón para procesar
button_procesar = ttk.Button(root, text="Procesar Archivos", command=procesar)
button_procesar.grid(row=3, column=0, columnspan=3, pady=20)

# Iniciar el bucle principal de la aplicación
root.mainloop()
