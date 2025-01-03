import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from config.env import init_env
# CONFIGURACIÓN INICIAL
init_env()

# Crear la aplicación de PyQt5
app = QApplication(sys.argv)

from ui.schema.main_window import MainWindow
from ui.logs import configurar_logger, get_logger

# Crear la ventana principal
main_window = MainWindow()

# Configurar el logger global y vincularlo al LoggerBox de la UI
configurar_logger(main_window.ui.LoggerBox)
actualizar_log = get_logger()


# Agregar un mensaje inicial al log
actualizar_log("Aplicación iniciada.")

# Mostrar la ventana principal
main_window.show()

# Función para manejar el cierre de la ventana
def on_closing():
    respuesta = QMessageBox.question(main_window, "Confirmar cierre", "¿Estás seguro de que deseas cerrar la ventana?", QMessageBox.Yes | QMessageBox.No)
    if respuesta == QMessageBox.Yes:
        actualizar_log("Finalizando Procesos")
        app.quit()  # Terminar la aplicación

# Conectar el evento de cierre de la ventana
main_window.closeEvent = lambda event: (on_closing(), event.accept())

# Iniciar el bucle principal de la aplicación
sys.exit(app.exec_())
