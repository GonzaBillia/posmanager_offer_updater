import tkinter as tk

class PrintRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        if message != '\n':
            self.widget.insert(tk.END, message + '\n')
            self.widget.yview(tk.END)

    def flush(self):
        pass

def configurar_logs(root):
    # Crear el área de texto para los logs
    log_area = tk.Text(root, height=10, width=100, wrap=tk.WORD, state=tk.DISABLED)
    log_area.grid(row=5, column=0, columnspan=3, pady=10)
    
    # Función anidada para actualizar logs
    def actualizar_log(message):
        log_area.config(state=tk.NORMAL)  # Hacer el área de texto editable temporalmente
        log_area.insert(tk.END, message + '\n')  # Insertar el mensaje con salto de línea
        log_area.yview(tk.END)  # Desplazar hacia abajo
        log_area.config(state=tk.DISABLED)  # Deshabilitar la edición
        root.update()  # Actualizar la interfaz
    
    return log_area, actualizar_log
