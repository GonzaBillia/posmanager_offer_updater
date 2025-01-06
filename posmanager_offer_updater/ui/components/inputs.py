from PyQt5.QtWidgets import QFileDialog, QCheckBox
from ui.components.logs import get_logger
from ui.components.filters import config
import os

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def seleccionar_archivo_entrada2(entry_archivo2):
    file_path, _ = QFileDialog.getOpenFileName(None, "Seleccionar la lista de Items de POSManager", "", "Archivos TXT (*.txt);;Archivos CSV (*.csv);;Archivos Excel (*.xlsx *.xls)")
    if file_path:
        entry_archivo2.setText(file_path)
        actualizar_log(f"Lista de Items de POSManager seleccionada: {file_path}")

def seleccionar_archivo_propuesta(entry_propuesta):
    file_path, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo de Propuesta", "", "Archivos Excel (*.xlsx *.xls)")
    if file_path:
        entry_propuesta.setText(file_path)
        actualizar_log(f"Archivo de Propuesta seleccionado: {file_path}")


def crear_inputs(ui):
    default_propuesta = os.path.expanduser('~\\Documents\\PM-offer-updater\\import\\Propuesta.xlsx')

    # Conectar los botones existentes en la UI con las funciones de selección de archivo
    ui.button_items.clicked.connect(lambda: seleccionar_archivo_entrada2(ui.input_items))
    ui.button_propuesta.clicked.connect(lambda: seleccionar_archivo_propuesta(ui.input_propuesta))

    ui.input_propuesta.setText(default_propuesta)

    return ui.input_items, ui.input_propuesta

