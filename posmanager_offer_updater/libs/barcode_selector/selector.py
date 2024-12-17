import pandas as pd
import os
from datetime import datetime
from tkinter import filedialog, messagebox
import unicodedata

def seleccionar_barcodes(output_file, barcode_query):
    try:
        #Lectura de archivos
        try:
            df1 = pd.read_csv(output_file)
            df2 = pd.read_csv(barcode_query, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los archivos: {e}")
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
            print(f"Error: Las siguientes columnas no se encuentran en df1: {', '.join(missing_columns_df1)}")
            exit()

        if missing_columns_df2:
            print(f"Error: Las siguientes columnas no se encuentran en df2: {', '.join(missing_columns_df2)}")
            exit()
        
        # Realizar el "merge" entre las dos tablas usando 'CodigoERP', con un 'left join' para incluir filas de df1 que no están en df2
        merged_df = pd.merge(df1[['IDProducto', 'codigoInterno']], df2[['IDProducto', 'Codebar']], on='IDProducto', how='left')

        # Reordenar las columnas según la solicitud (codigoInterno, Codebar)
        result = merged_df[['codigoInterno', 'Codebar']]

        # OUTPUT

        # Carpeta de salida
        output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\codebars')

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Crear el nombre de archivo con la fecha de hoy
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        output_file = os.path.join(output_dir, f"CodBarras-{fecha_hoy}.txt")

        # Guardar el resultado
        result.to_csv(output_file, sep='\t', index=False, header=False)

        return output_file

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        return False
