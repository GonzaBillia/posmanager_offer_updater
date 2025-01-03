# -*- coding: utf-8 -*-

# Archivo principal modularizado

from PyQt5 import QtWidgets, QtCore
from ui.schema.main_window_ui import Ui_main  # Archivo generado por pyuic5
from controllers.process_controller import process  # Importa la función desde el orquestador
from datetime import datetime
from controllers.file_controller import read_query_config, save_query_config
from ui.logs import configurar_logger, get_logger  # Configurar logger correctamente

# Leer configuración inicial
config = read_query_config()
if config is None:
    config = {}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.setup_logger()
        self.setup_connections()
        self.load_initial_config()

    def setup_logger(self):
        """
        Configura el logger global y lo vincula al LoggerBox de la UI.
        """
        configurar_logger(self.ui.LoggerBox)
        self.actualizar_log = get_logger()
        self.actualizar_log("Logger configurado correctamente.")

    def setup_connections(self):
        """
        Configura los signals y slots.
        """
        self.ui.button_procesar.clicked.connect(self.process_files)
        self.ui.button_items.clicked.connect(self.select_items_file)
        self.ui.button_propuesta.clicked.connect(self.select_propuesta_file)
        self.ui.check_re_etiquetado.stateChanged.connect(self.update_re_etiqueta_var)

    def load_initial_config(self):
        """
        Carga la configuración inicial de los filtros.
        """
        dias_guardados = config.get('dias', datetime.now().strftime('%Y-%m-%d'))
        try:
            fecha_dias = datetime.strptime(dias_guardados, '%Y-%m-%d').date()
        except ValueError:
            self.actualizar_log(f"Fecha inválida en configuración: {dias_guardados}. Usando fecha actual.")
            fecha_dias = datetime.now().date()

        self.ui.date_fecha.setDate(fecha_dias)
        self.ui.check_re_etiquetado.setChecked(config.get('optimizar_etiquetas', False))
        self.ui.check_categories.setChecked(config.get('dpts_fams', False))

    def select_items_file(self):
        """
        Abre un cuadro de diálogo para seleccionar el archivo de items.
        """
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Seleccionar Archivo de Items", "", "Archivos CSV (*.csv);;Archivos de Texto (*.txt);;Todos los archivos (*)")
        if file_name:
            self.ui.input_items.setText(file_name)

    def select_propuesta_file(self):
        """
        Abre un cuadro de diálogo para seleccionar el archivo de propuesta comercial.
        """
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Seleccionar Archivo de Propuesta", "", "Archivos CSV (*.csv);;Archivos de Texto (*.txt);;Todos los archivos (*)")
        if file_name:
            self.ui.input_propuesta.setText(file_name)

    def update_re_etiqueta_var(self):
        """
        Actualiza la variable relacionada con el CheckBox de re-etiquetado.
        """
        re_etiqueta_var = self.ui.check_re_etiquetado.isChecked()
        self.actualizar_log(f"Re-etiquetado actualizado a: {'Activado' if re_etiqueta_var else 'Desactivado'}")

    def process_files(self):
        """
        Lógica para procesar los archivos seleccionados mediante el controlador.
        """
        items_file = self.ui.input_items.text()
        propuesta_file = self.ui.input_propuesta.text()

        if not items_file or not propuesta_file:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, selecciona ambos archivos antes de procesar.")
            return

        try:
            process(items_file, propuesta_file, self.ui.check_re_etiquetado.isChecked())
            self.actualizar_log(f"Archivos procesados correctamente:\n- {items_file}\n- {propuesta_file}")
            self.ui.progressBar.setValue(100)
            self.save_config()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al procesar los archivos: {str(e)}")

    def save_config(self):
        """
        Guarda la configuración actual de los filtros.
        """
        fecha_seleccionada = self.ui.date_fecha.date().toString('yyyy-MM-dd')
        nueva_configuracion = {
            'dias': fecha_seleccionada,
            'optimizar_etiquetas': self.ui.check_re_etiquetado.isChecked(),
            'dpts_fams': self.ui.check_categories.isChecked()
        }
        config.update(nueva_configuracion)
        self.actualizar_log("Configuración guardada exitosamente.")
