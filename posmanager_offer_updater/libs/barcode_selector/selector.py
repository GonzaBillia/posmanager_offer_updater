import pandas as pd
import os
from datetime import datetime
from tkinter import messagebox
from ui.components.logs import get_logger

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def seleccionar_barcodes(output_file, barcode_query):
    try:
        #Lectura de archivos
        try:
            df1 = pd.read_csv(output_file)
            df2 = pd.read_csv(barcode_query, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los archivos: {e}")
            actualizar_log(f"Error al leer los archivos: {e}")
            return

        # Limpiar los nombres de las columnas eliminando espacios en blanco
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()

        # Verificar que las columnas necesarias existen en ambos DataFrames
        required_columns_df1 = ['IDProducto']
        required_columns_df2 = ['IDProducto']

        missing_columns_df1 = [col for col in required_columns_df1 if col not in df1.columns]
        missing_columns_df2 = [col for col in required_columns_df2 if col not in df2.columns]

        if missing_columns_df1:
            actualizar_log(f"Error: Las siguientes columnas no se encuentran en df1: {', '.join(missing_columns_df1)}")
            return

        if missing_columns_df2:
            actualizar_log(f"Error: Las siguientes columnas no se encuentran en df2: {', '.join(missing_columns_df2)}")
            return
        
        # Realizar el "merge" entre las dos tablas usando 'CodigoERP', con un 'left join' para incluir filas de df1 que no están en df2
        merged_df = pd.merge(df1[['IDProducto', 'codigoInterno']], df2[['IDProducto', 'Codebar']], on='IDProducto', how='left')

        # Reordenar las columnas según la solicitud (codigoInterno, Codebar, IDProducto para filtrar)
        result = merged_df[['IDProducto', 'codigoInterno', 'Codebar']]

        # Eliminar duplicados
        result = result.drop_duplicates()

        # 🔥 Eliminar todas las filas donde IDProducto sea menor a 8000
        result = result[result['IDProducto'] >= 8000]

        # Quitar IDProducto si no quieres que aparezca en el output final
        result = result[['codigoInterno', 'Codebar']]
        
        actualizar_log("Cruce de archivo de codigo de barras realizado")

        # OUTPUT

        # Carpeta de salida
        output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\processed-files\\Codebars')

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Crear el nombre de archivo con la fecha de hoy
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        output_file = os.path.join(output_dir, f"CodBarras-{fecha_hoy}.txt")

        # Guardar el resultado
        result.to_csv(output_file, sep='\t', index=False, header=False)

        # Aviso del archivo creado
        actualizar_log(f"Archivo procesado y guardado en {output_file}")
        actualizar_log("---------- Proceso de preparacion de codigo de barras Terminado ----------")

        return output_file

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        actualizar_log(f"Ocurrió un error: {e}")
        return False
