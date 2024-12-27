from controllers.query_controller import quantio_updated_departments, quantio_updated_families, quantio_updated_providers
from controllers.file_controller import save_direct_file
from ui.logs import get_logger

actualizar_log = get_logger()

def process_categories_files(connection):
    try:
        data_provs = quantio_updated_providers(connection)
        data_dpts = quantio_updated_departments(connection)
        data_fams = quantio_updated_families(connection)
        output_file_provs = save_direct_file(data_provs, "Proveedores")
        output_file_dpts = save_direct_file(data_dpts, "Departamentos")
        output_file_fams = save_direct_file(data_fams, "Familias")
        actualizar_log("Los Archivos se procesaron correctamente")
        return output_file_dpts, output_file_fams, output_file_provs
    except Exception as e:
        actualizar_log(f"Ocurrio un Error en el proceso de las consultas: {e}")
        raise e
