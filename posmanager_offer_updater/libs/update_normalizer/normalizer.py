import pandas as pd
import os, csv
from datetime import datetime
from ui.components.logs import get_logger

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def detectar_delimitador(file_path):
    """Detecta el delimitador del archivo usando csv.Sniffer"""
    try:
        with open(file_path, 'r', encoding='latin1') as f:
            sample = f.read(2048)  # Leer una muestra del archivo
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            return dialect.delimiter
    except Exception as e:
        actualizar_log(f"No se pudo detectar el delimitador automáticamente: {e}")
        return None  # Devolver None si hay un error

def procesar_archivos(file_path1, file_path2):
    # Intentar leer los archivos
    try:
        # Leer el archivo df1 (CSV delimitado por tabulaciones)
        df1 = pd.read_csv(file_path1, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
    except pd.errors.ParserError as e:
        actualizar_log(f"Error de análisis al leer el archivo {file_path1}: {e}")
        return
    except FileNotFoundError as e:
        actualizar_log(f"Archivo no encontrado: {file_path1}")
        return
    except Exception as e:
        actualizar_log(f"Hubo un error al leer el archivo {file_path1}: {e}")
        return


    try:
        # Intentar detectar el delimitador
        delim = detectar_delimitador(file_path2)

        if delim is None:
            actualizar_log(f"No se detectó delimitador válido para el archivo {file_path2}, intentando con tabulación por defecto.")
            delim = '\t'  # Asignar tabulación como opción de respaldo

        # Leer el archivo con el delimitador detectado
        df2 = pd.read_csv(file_path2, 
                        sep=delim, 
                        encoding='latin1',
                        on_bad_lines='skip')

        # Verificar si la detección del delimitador es correcta
        if df2.shape[1] == 1:  # Si solo hay una columna, el delimitador puede ser incorrecto
            actualizar_log(f"Posible error al detectar el delimitador en {file_path2}. "
                        f"Se leyó como una sola columna con '{delim}', intentando con otro delimitador.")

            # Intentar con la tabulación si el delimitador inicial fue una coma
            nuevo_delim = ',' if delim == '\t' else '\t'
            df2 = pd.read_csv(file_path2, 
                            sep=nuevo_delim, 
                            encoding='latin1',
                            on_bad_lines='skip')

            # Verificar nuevamente si sigue fallando
            if df2.shape[1] == 1:
                actualizar_log(f"Error: No se pudo determinar correctamente el delimitador en {file_path2}.")
                return

    except pd.errors.ParserError as e:
        actualizar_log(f"Error de análisis al leer el archivo {file_path2}: {e}")
        return
    except FileNotFoundError as e:
        actualizar_log(f"Archivo no encontrado: {file_path2}")
        return
    except Exception as e:
        actualizar_log(f"Hubo un error al leer el archivo {file_path2}: {e}")
        return

    # NORMALIZACION Y JOIN

    # Limpiar los nombres de las columnas eliminando espacios en blanco
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Verificar que las columnas necesarias existen en ambos DataFrames
    required_columns_df1 = ['IDProducto']
    required_columns_df2 = ['CodigoERP']

    missing_columns_df1 = [col for col in required_columns_df1 if col not in df1.columns]
    missing_columns_df2 = [col for col in required_columns_df2 if col not in df2.columns]

    if missing_columns_df1:
        actualizar_log(f"Error: Las siguientes columnas no se encuentran en df1: {', '.join(missing_columns_df1)}")
        return

    if missing_columns_df2:
        actualizar_log(f"Error: Las siguientes columnas no se encuentran en df2: {', '.join(missing_columns_df2)}")
        return


    # Renombrar la columna 'IDProducto' de df1 a 'CodigoERP'
    df2 = df2.rename(columns={'CodigoERP': 'IDProducto'})

    # Lista de columnas a mostrar en el orden especificado
    columnas_a_mostrar = [
        'codigoInterno', 'IdItem', 'Nom Reducido', 'idItem', 'idTipoIVA', 'idCategoria',
        'IDSubRubro', 'Codigo_de_Envase_asociado', 'Porc_de_Impuesto_Interno',
        'precio_final', 'FechaUltimoPrecio', 'descrip reducida',
        'Eliminacion_de_item', 'Tipo de Unidad', 'Unidad', 'Dias_de_Vencimiento',
        'Tamanio de Letra', 'FechaUltimoPrecio', 'Codigo_Adicional',
        'Permite_Modif_Descripcion', 'Precio adicional de venta con IVA',
        'Codigo de Plantilla de Etiqueta', 'Codigo de IVA Diferencial',
        'UltimoPrecio', 'Precio_de_Oferta_Etiquetas', 'IDProducto',
        'Codigo_de_envase_asociado_ERP', 'Monto_de_Impuesto_Interno', 'idTipoIVA',
        'Aplica_Percepcion_5329', 'Costo _el_articulo', 'idProveedor',
        'IDRubro', 'idMarca', 'Fecha Inicio', 'Fecha Fin'
    ]

    # Realizar el "merge" entre las dos tablas usando 'CodigoERP', con un 'left join' para incluir filas de df1 que no están en df2
    merged_df = pd.merge(df1, df2[['IDProducto', 'IdItem']], on='IDProducto', how='left')

    # Reordenar las columnas según la solicitud (CodigoERP, codigoInterno, idItem)
    result = merged_df[columnas_a_mostrar]

    actualizar_log("Cruce de archivos realizado")

    # ID GENERATOR

    # Crear un conjunto de todos los valores existentes en df2['IdItem'] para evitar duplicados
    existing_ids = set(df2['IdItem'].dropna().astype(int))

    # Identificar los índices donde 'idItem' está vacío
    empty_id_indices = result[result['IdItem'].isna()].index

    # Calculamos el número exacto de IDs necesarios
    required_ids = len(empty_id_indices)  # Número de filas que necesitan IDs

    # Aseguramos un rango suficientemente amplio
    new_ids = (id for id in range(8000, 8000 + required_ids + len(existing_ids)) if id not in existing_ids)

    # Asignamos nuevos valores a las filas faltantes
    for index in empty_id_indices:
        codigo_interno = result.at[index, 'codigoInterno']
        
        if pd.notna(codigo_interno) and int(codigo_interno) < 8000:
            # Si codigoInterno es menor a 8000, asignamos ese valor a IdItem
            result.at[index, 'IdItem'] = int(codigo_interno)
        else:
            # De lo contrario, asignamos un nuevo ID único
            result.at[index, 'IdItem'] = next(new_ids)

    # Mostramos la cantidad de codigos creados
    actualizar_log(f"Codigos creados: {required_ids}")

    # Convertimos la columna IdItem a enteros, manejando los NaN
    result['IdItem'] = result['IdItem'].fillna(0).astype(int)

    # ID GENERATOR


    result = result.drop(columns=['codigoInterno'])
    # Renombrar 'IdItem' como 'codigoInterno'
    result.rename(columns={'IdItem': 'codigoInterno'}, inplace=True)

    # Aplicar la transformación de descripcion según las condiciones
    result['Nom Reducido'] = result.apply(
        lambda row: row['Nom Reducido'].replace(" X G", " X KG") 
        if row['Nom Reducido'].endswith(" X G") and row['codigoInterno'] < 8000 
        else row['Nom Reducido'], 
        axis=1
    )

    # OUTPUT

     # Carpeta de salida
    output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\processed-files\\Items')

    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Crear el nombre de archivo con la fecha de hoy
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f"Items-{fecha_hoy}.csv")

    # Guardar el resultado
    result.to_csv(output_file, index=False)

    #Aviso del archivo creado
    actualizar_log(f"Archivo procesado y guardado en {output_file}")
    actualizar_log("---------- Proceso de normalizacion Terminado ----------")

    return output_file