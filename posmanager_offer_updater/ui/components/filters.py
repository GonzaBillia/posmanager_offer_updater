from PyQt5.QtWidgets import QFileDialog, QCheckBox, QMessageBox
from PyQt5.QtCore import QDateTime
from ui.components.logs import get_logger
from controllers.file_controller import read_query_config, save_query_config
import os

# Obtener la función para actualizar logs
actualizar_log = get_logger()
config = None

def actualizar_ui_con_configuracion(ui):
    global config
    # Leer configuración
    config = read_query_config()
    # Inicializar configuración si está vacía
    if config is None:
        config = {}

    if config:
        ui.progressBar.setValue(0)
        ui.progressBar.setDisabled(True)
        ui.button_option_propuesta.setEnabled(False)
        ui.label_seleccion_propuesta.setVisible(False)
        ultima_fecha = config.get("timestamp", "No disponible")
        fecha = config.get('dias')
        ui.label_ult_fecha.setText(f"{ultima_fecha}")
        ui.date_fecha.setDateTime(QDateTime.fromString(fecha, "yyyy-MM-dd HH:mm"))
        ui.check_ultima_fecha.setChecked(config.get('usar_timestamp', False))
        ui.check_categories.setChecked(config.get('dpts_fams', False))
        
        # Conectar el evento después de cargar la UI
        ui.check_ultima_fecha.stateChanged.connect(lambda: ui.date_fecha.setDisabled(ui.check_ultima_fecha.isChecked()))

        if ui.check_ultima_fecha.isChecked():
            ui.date_fecha.setDisabled(True)
        
        # Función para habilitar o deshabilitar el botón según el índice seleccionado
        def toggle_button_option_propuesta():
            if ui.dropdown_option_propuesta.currentIndex() == 2:  # Índice 2
                ui.button_option_propuesta.setEnabled(True)
                ui.label_seleccion_propuesta.setVisible(True)
                ui.label_seleccion_propuesta.setText("preview.xlsx")
            else:
                ui.button_option_propuesta.setEnabled(False)
                ui.label_seleccion_propuesta.setVisible(False)

        # Conectar la señal del dropdown a la función de control
        ui.dropdown_option_propuesta.currentIndexChanged.connect(toggle_button_option_propuesta)



def ventana_query_quantio(ui):
    # Leer configuración actual

    actualizar_ui_con_configuracion(ui)

    def save_config():

        # Obtener los valores de la UI
        fecha_seleccionada = ui.date_fecha.dateTime().toString("yyyy-MM-dd HH:mm")
        usar_ultima_fecha = ui.check_ultima_fecha.isChecked()
        usar_categorias = ui.check_categories.isChecked()

        # Crear el diccionario de configuración
        nueva_configuracion = {
            'dias': fecha_seleccionada,
            'usar_timestamp': usar_ultima_fecha,
            'dpts_fams': usar_categorias
        }

        # Actualizar y guardar la configuración
        config.update(nueva_configuracion)
        save_query_config(config)

    # Conectar el botón de guardar con la función
    ui.button_procesar.clicked.connect(save_config)


