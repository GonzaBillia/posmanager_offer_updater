import pandas as pd
import os
from ui.components.logs import get_logger

actualizar_log = get_logger()

def filter_by_proposal(proposal):
    # Leer archivos
    try:
        carpeta = os.path.expanduser(f'~\\Documents\\PM-offer-updater\\processed-files\\History\\Propuesta')

        # Obtener la lista de archivos
        archivos = os.listdir(carpeta)

        # Filtrar solo archivos (excluyendo carpetas) y obtener el primero
        last_proposal = [f for f in archivos if os.path.isfile(os.path.join(carpeta, f))][0]
        df1 = pd.read_excel(proposal)
        df2 = pd.read_excel(last_proposal)

        list1 = df1.iloc[:, 0].tolist()
        list1_2 = df1.iloc[:, 1].tolist()
        list2 = df2.iloc[:, 0].tolist()
        list2_2 = df2.iloc[:, 1].tolist()

        dif_list = [
            (id_nuevo, valor_nuevo) 
            for id_nuevo, valor_nuevo in zip(list1, list1_2)
            if id_nuevo not in list2 or valor_nuevo != list2_2[list2.index(id_nuevo)]
        ]

        return dif_list
        
    except Exception as e:
        actualizar_log("Error al leer los archivos para calcular")
        return

def filter_fixed_price(proposal):
    try:
        df1 = pd.read_excel(proposal)

        list1 = df1.iloc[:, 0].tolist()

        fixed_list = [item for item in list1 if item > 1]

        return fixed_list
        
    except Exception as e:
        actualizar_log("Error al leer los archivos para calcular")
        return

def filter_discount_price(proposal):
    try:
        df1 = pd.read_excel(proposal)

        list1 = df1.iloc[:, 0].tolist()

        fixed_list = [item for item in list1 if item < 1]

        return fixed_list
        
    except Exception as e:
        actualizar_log("Error al leer los archivos para calcular")
        return
    
def filter_by_offer(proposal):
    try:
        df1 = pd.read_excel(proposal)

        list1 = df1.iloc[:, 0].tolist()

        return list1
        
    except Exception as e:
        actualizar_log("Error al leer los archivos para calcular")
        return
    

    