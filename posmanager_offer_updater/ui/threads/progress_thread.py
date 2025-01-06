from PyQt5.QtCore import QThread, pyqtSignal

class ThreadProgress(QThread):
    # Señal para actualizar la barra de progreso
    progreso_actualizado = pyqtSignal(int)

    def __init__(self, pasos_totales, parent=None):
        super().__init__(parent)
        self.pasos_totales = pasos_totales
        self.paso_actual = 0
        self.running = True

    def run(self):
        """
        Método principal de ejecución del hilo.
        """
        while self.running and self.paso_actual < self.pasos_totales:
            self.paso_actual += 1
            porcentaje = int((self.paso_actual / self.pasos_totales) * 100)
            self.progreso_actualizado.emit(porcentaje)

    def detener(self):
        """
        Detiene el hilo de ejecución.
        """
        self.running = False
