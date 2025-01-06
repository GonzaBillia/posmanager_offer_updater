import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.schema.main_window import Ui_main
from ui.components.logs import configurar_logger, get_logger
from config.env import init_env

# CONFIGURACION INICIAL DE LA VENTANA
init_env()

# Crear la aplicación y la ventana principal
app = QApplication(sys.argv)
ui = Ui_main()
window = QMainWindow()
ui.setupUi(window)

# Configurar el logger global y obtener la función para actualizar logs
try:
    log_config = configurar_logger(ui)
    actualizar_log = get_logger()
except RuntimeError as e:
    print(f"Error: {e}")
    actualizar_log = print  # Reemplazo temporal para evitar fallos críticos


# Función para manejar el cierre de la ventana
def on_closing(event):
    respuesta = QMessageBox.question(
        window,
        "Confirmar cierre",
        "¿Estás seguro de que deseas cerrar la ventana?",
        QMessageBox.Yes | QMessageBox.No
    )
    if respuesta == QMessageBox.Yes:
        actualizar_log("Finalizando Procesos")
        event.accept()  # Permitir que la ventana se cierre
    else:
        event.ignore()  # Evitar que la ventana se cierre

# Conectar el evento de cierre de la ventana
window.closeEvent = on_closing

if actualizar_log is not None:
    # CONFIGURACION INICIAL DE DB Y ELEMENTOS UI
    from ui.components.inputs import crear_inputs
    from ui.components.buttons import crear_botones
    from ui.components.filters import ventana_query_quantio

    entry_archivo2, entry_propuesta = crear_inputs(ui)
    ventana_query_quantio(ui)
    button_procesar = crear_botones(ui, entry_archivo2, entry_propuesta)

    # Agregar un mensaje inicial al log
    actualizar_log("Aplicación iniciada")

    # Mostrar la ventana principal
    window.show()

    # Iniciar el bucle principal de la aplicación
    sys.exit(app.exec_())
