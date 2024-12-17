import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Crear una ventana oculta de Tkinter
Tk().withdraw()


# INPUT

# Solicitar al usuario que seleccione el primer archivo (df1)
print("Selecciona el archivo para la primera tabla (archivo 1 - CSV delimitado por tabulaciones):")
file_path1 = askopenfilename(title="Seleccionar el primer archivo", filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])

# Solicitar al usuario que seleccione el segundo archivo (df2)
print("Selecciona el archivo para la segunda tabla (archivo 2 - TXT delimitado por comas):")
file_path2 = askopenfilename(title="Seleccionar el segundo archivo", filetypes=[("Archivos TXT", "*.txt"), ("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])

# Intentar leer los archivos
try:
    # Leer el archivo df1 (CSV delimitado por tabulaciones)
    df1 = pd.read_csv(file_path1, sep='\t', encoding='latin1', on_bad_lines='skip')

    # Leer el archivo df2 (TXT delimitado por comas)
    df2 = pd.read_csv(file_path2, sep=',', encoding='latin1', on_bad_lines='skip')

except Exception as e:
    print(f"Hubo un error al leer los archivos: {e}")
    exit()

# INPUT


# NORMALIZACION Y JOIN

# Reparar posibles problemas de codificación en 'Nom Reducido'
df1['Nom Reducido'] = df1['Nom Reducido'].str.encode('latin1').str.decode('utf-8')

# Limpiar los nombres de las columnas eliminando espacios en blanco
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Verificar que las columnas necesarias existen en ambos DataFrames
if 'IDProducto' not in df1.columns or 'CodigoERP' not in df2.columns:
    print("Error: Las columnas 'IDProducto' o 'CodigoERP' no se encuentran en ambos archivos.")
    exit()

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

columnas_a_mostrar_final = [
    'codigoInterno', 'Nom Reducido', 'idItem', 'idTipoIVA', 'idCategoria',
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

# Convertimos la columna IdItem a enteros, manejando los NaN
result['IdItem'] = result['IdItem'].fillna(0).astype(int)

# ID GENERATOR

result = result.drop(columns=['codigoInterno'])
# Renombrar 'IdItem' como 'codigoInterno'
result.rename(columns={'IdItem': 'codigoInterno'}, inplace=True)

# Reorganizar las columnas
result = result[columnas_a_mostrar_final]

# OUTPUT

# Solicitar al usuario que elija el nombre y ubicación para guardar el archivo de salida
print("\nSelecciona el lugar donde guardar el archivo de resultado:")
output_file = asksaveasfilename(title="Guardar archivo de resultado", defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")])

# Verificar si el usuario seleccionó una ruta válida
if output_file:
    # Guardar el resultado en el archivo seleccionado
    if output_file.endswith(('.xls', '.xlsx')):
        result.to_excel(output_file, index=False)
    else:
        result.to_csv(output_file, index=False)

    print("El archivo de resultados ha sido guardado exitosamente.")
else:
    print("No se seleccionó ningún archivo para guardar.")
