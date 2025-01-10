import pandas as pd
import os
from ui.components.logs import get_logger

actualizar_log = get_logger()

def filter_by_proposal(proposal):
    try:
        carpeta = os.path.expanduser(f'~\\Documents\\PM-offer-updater\\processed-files\\History\\Propuesta')

        # Obtener la lista de archivos
        archivos = os.listdir(carpeta)

        # Filtrar solo archivos y obtener el más reciente
        last_proposal = [f for f in archivos if os.path.isfile(os.path.join(carpeta, f))][0]

        # Leer los archivos de Excel
        df1 = pd.read_excel(proposal)
        df2 = pd.read_excel(os.path.join(carpeta, last_proposal))

        # Eliminar filas con NaN en las dos primeras columnas
        df1 = df1.dropna(subset=[df1.columns[0], df1.columns[1]])
        df2 = df2.dropna(subset=[df2.columns[0], df2.columns[1]])

        # Convertir las columnas a diccionarios
        dict1 = dict(zip(df1.iloc[:, 0].astype(int).tolist(), df1.iloc[:, 1].tolist()))
        dict2 = dict(zip(df2.iloc[:, 0].astype(int).tolist(), df2.iloc[:, 1].tolist()))

        # Lista para almacenar los IDs que difieren
        dif_list = set()

        # Detectar IDs en dict1 pero no en dict2 o con valores diferentes
        for id_nuevo, valor_nuevo in dict1.items():
            if id_nuevo not in dict2 or valor_nuevo != dict2.get(id_nuevo):
                dif_list.add(id_nuevo)

        # Detectar IDs en dict2 pero no en dict1
        for id_antiguo in dict2.keys():
            if id_antiguo not in dict1:
                dif_list.add(id_antiguo)

        # Convertir el conjunto a lista y mostrar el resultado
        dif_list = list(dif_list)

        return dif_list

    except Exception as e:
        actualizar_log(f"Error al leer los archivos para calcular: {e}")
        return

    
def filter_by_offer(proposal):
    try:
        df1 = pd.read_excel(proposal)
        df1 = df1.dropna(subset=[df1.columns[0], df1.columns[1]])
        
        list1 = df1.iloc[:, 0].astype(int).tolist()

        return list1
        
    except Exception as e:
        actualizar_log("Error al leer los archivos para calcular")
        return
    

    