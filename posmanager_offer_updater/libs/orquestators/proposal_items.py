from libs.proposal_filterer.filterer import filter_by_proposal, filter_by_offer
from controllers.query_controller import quantio_selected_products
from controllers.file_controller import guardar_resultados_como_csv
from ui.components.logs import get_logger
import pandas as pd

actualizar_log = get_logger()

file_path = "raw\\quantio\\items"
name = "Items"

def process_proposal(proposal, option, price_changes, connection):
    filtered_list = None
    if option == 1:
        filtered_list = filter_by_offer(proposal)
    elif option == 2:
        filtered_list = filter_by_proposal(proposal)
    else:
        pass

    try:
        df1 = pd.read_csv(price_changes, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
        price_list = df1['IDProducto'].tolist()

        # Inicializa filtered_list como lista vacía si es None
        if filtered_list is None:
            filtered_list = []

        # Extiende la lista filtrada con los valores de price_list
        filtered_list.extend(price_list)
        # Elimina duplicados
        final_list = list(dict.fromkeys(filtered_list))

        data = quantio_selected_products(final_list, connection)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        actualizar_log("El archivo Items Quantio se procesó correctamente")
        return output_file
    except Exception as e:
        actualizar_log(f"Ocurrió un Error en el proceso de la consulta: {e}")
        raise e
    