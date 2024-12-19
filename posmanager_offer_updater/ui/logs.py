import tkinter as tk

# Variables globales para el logger
log_area = None
actualizar_log = None

class PrintRedirector:
    """
    Redirige la salida de `print` a un widget de texto.
    """
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        if message.strip():  # Evitar mensajes vacíos
            self.widget.insert(tk.END, message + '\n')
            self.widget.yview(tk.END)

    def flush(self):
        pass

def configurar_logger(root):
    """
    Configura el logger global y define las funciones necesarias.
    """
    global log_area, actualizar_log

    # Crear el área de logs
    log_area = tk.Text(root, height=10, width=100, wrap=tk.WORD, state=tk.DISABLED)
    log_area.grid(row=5, column=0, columnspan=3, pady=10)

    # Definir la función para actualizar los logs
    def log(message):
        log_area.config(state=tk.NORMAL)
        log_area.insert(tk.END, message + '\n')
        log_area.yview(tk.END)
        log_area.config(state=tk.DISABLED)
        root.update()

    # Asignar la función al logger global
    actualizar_log = log

def get_logger():
    """
    Devuelve la función `actualizar_log` para usar en otros módulos.
    """
    if actualizar_log is None:
        raise RuntimeError("El logger no ha sido configurado. Llama a `configurar_logger` primero.")
    return actualizar_log
