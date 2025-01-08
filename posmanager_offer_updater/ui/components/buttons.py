from ui.components.logs import get_logger
from ui.components.filters import actualizar_ui_con_configuracion
from ui.components.inputs import get_option
from controllers.process_controller import process  # Importa la función desde el orquestador
from ui.threads.progress_thread import ThreadProgress

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def procesar(entry_archivo2, entry_propuesta, ui):
    # Crear la instancia del hilo de progreso
    hilo_progreso = ThreadProgress(pasos_totales=16)

    # Conectar la señal del hilo a la barra de progreso
    hilo_progreso.progreso_actualizado.connect(ui.progressBar.setValue)

    # Iniciar el hilo
    hilo_progreso.start
    ui.progressBar.setDisabled(False)
    ui.progressBar.setValue(0)
    
    file_path2 = entry_archivo2.text()
    file_propuesta = entry_propuesta.text()
    option = get_option(ui)

    # Llamar al orquestador para procesar los archivos
    process(file_path2, file_propuesta, option, hilo_progreso)
    actualizar_ui_con_configuracion(ui)

def crear_botones(ui, entry_archivo2, entry_propuesta):
    # Conectar el botón existente en la UI con la función procesar
    button_procesar = ui.button_procesar.clicked.connect(lambda: procesar(entry_archivo2, entry_propuesta,ui))
    return button_procesar