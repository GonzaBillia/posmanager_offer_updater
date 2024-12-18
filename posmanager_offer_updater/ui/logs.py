import sys
import tkinter as tk
from tkinter import scrolledtext

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
    log_area = tk.Text(root, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED)
    log_area.grid(row=5, column=0, columnspan=3, pady=10)
    
    return log_area

def actualizar_log(message, log_area):
    log_area.config(state=tk.NORMAL)  # Hacer el área de texto editable temporalmente
    log_area.insert(tk.END, message + '\n')  # Insertar el mensaje con salto de línea
    log_area.yview(tk.END)  # Desplazar hacia abajo
    log_area.config(state=tk.DISABLED)  # Deshabilitar la edición