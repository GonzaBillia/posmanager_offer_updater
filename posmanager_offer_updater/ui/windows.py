import tkinter as tk
from tkinter import ttk, Frame
from tkcalendar import DateEntry
from datetime import datetime
from ui.logs import get_logger

actualizar_log = get_logger()

def ventana_query_quantio(root):

    def calcular_dias():
        # Obtener la fecha seleccionada
        fecha_seleccionada = str(calendar.get_date())

        # Convertir la fecha seleccionada a un objeto datetime
        fecha_seleccionada = datetime.strptime(fecha_seleccionada, '%Y-%m-%d')

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Calcular la diferencia en días
        dias = (fecha_actual - fecha_seleccionada).days
        
        # Guardar la cantidad de días en una variable
        dias_variable = dias

        actualizar_log("Preferencias guardadas")

        ventana_query_quantio.destroy()

    # Crear la nueva ventana secundaria
    ventana_query_quantio = tk.Toplevel(root)
    ventana_query_quantio.title("Query Quantio")
    ventana_query_quantio.geometry("400x400")  # Tamaño de la nueva ventana

    # FRAMES

    frame_buttons = Frame(ventana_query_quantio)
    frame_buttons.pack(side="bottom", anchor="se", fill="x")

    frame_top_label = Frame(ventana_query_quantio)
    frame_top_label.pack(side="top", anchor="w", fill="x")

    frame_filters = Frame(ventana_query_quantio)
    frame_filters.pack(side="top", fill="both")

    sub_frame_date = Frame(frame_filters)
    sub_frame_date.pack(side="top", fill="x")



    # Etiqueta en la ventana secundaria
    label = tk.Label(frame_top_label, text="Control de Query")
    label.pack(side="left", pady=10, padx=10)
    

    check_include_meds = tk.BooleanVar(value=False)

    filter_meds = tk.Checkbutton(frame_filters, text="Incluir medicamentos", variable=check_include_meds)
    filter_meds.pack(side="top", anchor="w", padx=10, pady=10)

    # Descripción para el DateEntry
    label_date = tk.Label(sub_frame_date, text="Selecciona una fecha:")
    label_date.pack(side="left", padx=10, pady=5)  # Coloca la descripción encima del DateEntry

    # Calendar DateEntry
    calendar = DateEntry(sub_frame_date, date_pattern="mm/dd/yyyy", width=12, maxdate=datetime.now())
    calendar.pack(side="left", pady=10, padx=10)

    guardar_button = ttk.Button(frame_buttons, text="Guardar", command=lambda: calcular_dias())
    guardar_button.pack(side="right", pady=10, padx=10)

    # Botón para cerrar la ventana secundaria
    cerrar_button = ttk.Button(frame_buttons, text="Cerrar", command=lambda: ventana_query_quantio.destroy())
    cerrar_button.pack(side="right", pady=10, padx=10)

    return ventana_query_quantio
