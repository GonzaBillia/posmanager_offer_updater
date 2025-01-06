from PyQt5.QtWidgets import QFileDialog, QCheckBox, QMessageBox
from PyQt5.QtCore import QDate
from ui.components.logs import get_logger
from controllers.file_controller import read_query_config, save_query_config
import os

# Obtener la función para actualizar logs
actualizar_log = get_logger()
config = read_query_config()
re_etiqueta_var = False

# Inicializar configuración si está vacía
if config is None:
    config = {}

def set_re_etiqueta_var(state):
    global re_etiqueta_var
    re_etiqueta_var = state == 2

def revisar_var_etiqueta():
    return re_etiqueta_var

def actualizar_ui_con_configuracion(ui):
# Leer configuración
    config = read_query_config()
    if config:
        ui.progressBar.setValue(0)
        ui.progressBar.setDisabled(True)
        ultima_fecha = config.get("timestamp", "No disponible")
        fecha = config.get('dias')
        ui.label_ult_fecha.setText(f"{ultima_fecha}")
        ui.date_fecha.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))
        ui.check_ultima_fecha.setChecked(config.get('usar_timestamp', False))
        ui.check_labels.setChecked(config.get('optimizar_etiquetas', False))
        ui.check_categories.setChecked(config.get('dpts_fams', False))
        
        # Conectar el evento después de cargar la UI
        ui.check_ultima_fecha.stateChanged.connect(lambda: ui.date_fecha.setDisabled(ui.check_ultima_fecha.isChecked()))
        ui.check_re_etiquetado.stateChanged.connect(lambda state: set_re_etiqueta_var(state))

        if ui.check_ultima_fecha.isChecked():
            ui.date_fecha.setDisabled(True)


def ventana_query_quantio(ui):
    # Leer configuración actual
    global config

    actualizar_ui_con_configuracion(ui)

    def save_config():
        global config

        # Obtener los valores de la UI
        fecha_seleccionada = ui.date_fecha.date().toString("yyyy-MM-dd")
        usar_ultima_fecha = ui.check_ultima_fecha.isChecked()
        usar_optimizar_etiqueta = ui.check_labels.isChecked()
        usar_categorias = ui.check_categories.isChecked()

        # Crear el diccionario de configuración
        nueva_configuracion = {
            'dias': fecha_seleccionada,
            'usar_timestamp': usar_ultima_fecha,
            'optimizar_etiquetas': usar_optimizar_etiqueta,
            'dpts_fams': usar_categorias
        }

        # Actualizar y guardar la configuración
        config.update(nueva_configuracion)
        save_query_config(config)
        actualizar_log("Configuración guardada exitosamente.")

    # Conectar el botón de guardar con la función
    ui.button_procesar.clicked.connect(save_config)

    return re_etiqueta_var

