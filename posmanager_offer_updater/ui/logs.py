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
    log_area = scrolledtext.ScrolledText(root, width=100, height=15, wrap=tk.WORD)
    log_area.grid(row=6, column=0, columnspan=3, pady=20)
    
    # Redirigir los prints a este área de texto
    sys.stdout = PrintRedirector(log_area)
