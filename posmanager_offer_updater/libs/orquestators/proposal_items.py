from libs.proposal_filterer.filterer import filter_by_proposal, filter_discount_price, filter_fixed_price, filter_by_offer
from controllers.query_controller import quantio_selected_products
from controllers.file_controller import guardar_resultados_como_csv
from ui.components.logs import get_logger

actualizar_log = get_logger()

file_path = "raw\\quantio\\items"
name = "Items"

def process_proposal(proposal, option, connection):
    list = None
    if option == 1:
        list = filter_fixed_price(proposal)
    elif option == 2:
        list = filter_discount_price(proposal)
    elif option == 3:
        list = filter_by_offer(proposal)
    else:
        list = filter_by_proposal(proposal)

    try:
        data = quantio_selected_products(list, connection)
        output_file = guardar_resultados_como_csv(data, file_path, name)
        actualizar_log("El archivo Items Quantio se proceso correctamente")
        return output_file
    except Exception as e:
        actualizar_log(f"Ocurrio un Error en el proceso de la consulta: {e}")
        raise e
    