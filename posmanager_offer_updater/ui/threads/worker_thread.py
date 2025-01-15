from PyQt5.QtCore import QThread, pyqtSignal
from controllers.process_controller import process
import time  # Simulación de proceso pesado

# Hilo personalizado que ejecuta el proceso pesado
class WorkerThread(QThread):
    progreso_actualizado = pyqtSignal(int)

    def __init__(self, file_path2, file_propuesta, option, thread):
        super().__init__()
        self.file_path2 = file_path2
        self.file_propuesta = file_propuesta
        self.option = option
        self.thread_progreso = thread

    def run(self):
        process(self.file_path2, self.file_propuesta, self.option, self.thread_progreso)

