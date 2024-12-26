import tkinter as tk
from tkinter import ttk, Frame
from tkcalendar import DateEntry
from datetime import datetime
from controllers.file_controller import read_query_config, save_query_config
from ui.logs import get_logger

actualizar_log = get_logger()
config = read_query_config()

# Actualizar los valores existentes sin sobrescribir otras claves
if config is None:  # Si `config` no tiene datos, inicializa como un diccionario vacío
    config = {}

def ventana_query_quantio(root):

    # Variable de control para el Checkbutton
    timestamp_var = tk.BooleanVar(value=True)  # Inicialmente False
    optimize_var = tk.BooleanVar(value=False)

    def save_config():
        global config
       # Obtener la fecha seleccionada como string
        fecha_seleccionada = str(calendar.get_date())

        # Obtener el estado del Checkbutton
        usar_ultima_fecha = timestamp_var.get()
        usar_optimizar_etiqueta = optimize_var.get()

        # Crear el diccionario de configuración
        nueva_configuracion  = {
            'dias': fecha_seleccionada,
            'usar_timestamp': usar_ultima_fecha,
            'optimizar_etiquetas': usar_optimizar_etiqueta
        }


        config.update(nueva_configuracion)  # Actualiza `config` con las nuevas claves y valores

        # Guardar la configuración actualizada
        save_query_config(config)

        

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

    frame_timestamp = Frame(ventana_query_quantio)
    frame_timestamp.pack(side="top", fill="both")

    frame_optimize = Frame(ventana_query_quantio)
    frame_optimize.pack(side="top", fill="both")



    # Etiqueta en la ventana secundaria
    label = tk.Label(frame_top_label, text="Control de Query")
    label.pack(side="left", pady=10, padx=10)

    # Descripción para el DateEntry
    label_date = tk.Label(sub_frame_date, text="Selecciona una fecha:")
    label_date.pack(side="left", padx=10, pady=5)  # Coloca la descripción encima del DateEntry

    # Calendar DateEntry
    calendar = DateEntry(sub_frame_date, date_pattern="mm/dd/yyyy", width=12, maxdate=datetime.now())
    calendar.pack(side="left", pady=10, padx=10)

    timestamp_text = f"Usar ultima fecha de modificacion - {config.get('timestamp', 'N/A')}"
    timestamp = tk.Checkbutton(frame_timestamp, text=timestamp_text, variable=timestamp_var, indicatoron=True)    
    timestamp.pack(side='left', pady=10, padx=10)

    optimize_text = "Optimizar para etiquetas (filtra solo por cambio de precio)"
    optimize = tk.Checkbutton(frame_optimize, text=optimize_text, variable=optimize_var)
    optimize.pack(side='left', pady=10, padx=10)

    guardar_button = ttk.Button(frame_buttons, text="Guardar", command=lambda: save_config())
    guardar_button.pack(side="right", pady=10, padx=10)

    # Botón para cerrar la ventana secundaria
    cerrar_button = ttk.Button(frame_buttons, text="Cerrar", command=lambda: ventana_query_quantio.destroy())
    cerrar_button.pack(side="right", pady=10, padx=10)

    return ventana_query_quantio
