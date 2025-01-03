import sys
from PyQt5.QtWidgets import QListWidget

# Variable global para la función de log
actualizar_log = None

class PrintRedirector:
    """
    Redirige la salida de `print` a un QListWidget.
    """
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        if message.strip():  # Evitar mensajes vacíos
            self.widget.addItem(message)
            self.widget.scrollToBottom()

    def flush(self):
        pass


def configurar_logger(logger_box: QListWidget):
    """
    Configura el logger global para redirigir los mensajes al QListWidget.
    """
    global actualizar_log

    def log_message(message):
        try:
            logger_box.addItem(message)
            logger_box.scrollToBottom()
        except Exception as e:
            print(f"Error al actualizar el logger: {e}", file=sys.stderr)

    actualizar_log = log_message

    # Redirige `print` a la lista de logs
    sys.stdout = PrintRedirector(logger_box)
    sys.stderr = PrintRedirector(logger_box)


def get_logger():
    """
    Devuelve la función global `actualizar_log`. Si aún no está configurado,
    configura el logger automáticamente usando un QListWidget temporal.
    """
    global actualizar_log
    if actualizar_log is None:
        from PyQt5.QtWidgets import QListWidget
        logger_box = QListWidget()  # Crear un QListWidget temporal
        configurar_logger(logger_box)  # Configurar el logger con el QListWidget
        print("Logger configurado automáticamente.")
    return actualizar_log