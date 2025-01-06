from PyQt5.QtWidgets import QListWidget

# Variables globales para el logger
log_area = None
_actualizar_log = None

class PrintRedirector:
    """
    Redirige la salida de `print` a un widget de lista.
    """
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        if message.strip():  # Evitar mensajes vacíos
            self.widget.addItem(message)
            self.widget.scrollToBottom()

    def flush(self):
        pass

def configurar_logger(ui):
    """
    Configura el logger global y define las funciones necesarias.
    """
    global log_area, _actualizar_log

    try:
        # Asignar el área de logs existente en la UI
        log_area = ui.LoggerBox

        # Definir la función para actualizar los logs
        def log(message):
            try:
                log_area.addItem(message)
                log_area.scrollToBottom()
            except Exception as e:
                print(f"Error actualizando el logger: {e}")

        # Asignar la función al logger global
        _actualizar_log = log

        if _actualizar_log:
            # Mensaje de éxito para depuración
            print("Logger configurado correctamente")
            print(_actualizar_log)
            return _actualizar_log

    except Exception as e:
        print(f"Error configurando el logger: {e}")
        _actualizar_log = None
        return _actualizar_log

def get_logger():
    """
    Devuelve la función `_actualizar_log` para usar en otros módulos.
    """
    if _actualizar_log is None:
        raise RuntimeError("El logger no ha sido configurado. Llama a `configurar_logger` primero.")
    return _actualizar_log
