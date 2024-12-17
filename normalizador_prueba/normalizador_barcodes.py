import pandas as pd

tabla1 = 'plex_optimizado.csv'
tabla2 = 'posmanager_optimizado.csv'

# Leer los archivos CSV con codificación y delimitador explícitos
df1 = pd.read_csv(tabla1, encoding='latin1', sep=',')  # Cambiar sep si es necesario
df2 = pd.read_csv(tabla2, encoding='latin1', sep=';')  # Cambiar sep si es necesario

# Normalización de nombres de columnas
df1.columns = df1.columns.str.strip().str.lower().str.replace(r'[^\w\s]', '', regex=True)
df2.columns = df2.columns.str.strip().str.lower().str.replace(r'[^\w\s]', '', regex=True)

# Verificar columnas actuales en df2
print("Columnas de df2 después de ajustar el delimitador:", df2.columns)

# Renombrar columna correspondiente a 'cod_interno' si existe
if 'b' in df2.columns:
    df2 = df2.rename(columns={'b': 'cod_interno'})
elif 'cod_interno' in df2.columns:
    pass  # Ya está correctamente nombrada
else:
    raise KeyError("La columna 'B' o 'cod_interno' no está presente en df2 después de la normalización.")


# Transformar las columnas dinámicamente hasta 'codigo_16'
value_vars = [col for col in df2.columns if col.startswith('codigo_') and col <= 'codigo_16']
if not value_vars:
    raise KeyError("No se encontraron columnas que coincidan con 'codigo_' hasta 'codigo_16'.")

df2_long = df2.melt(
    id_vars=['cod_interno'], value_vars=value_vars,
    var_name='codigo_variable', value_name='codigo_producto'
)

# Filtrar filas donde 'codigo_producto' sea nulo o 0
df2_long = df2_long.dropna(subset=['codigo_producto'])
df2_long = df2_long[df2_long['codigo_producto'] != 0]

# Filtrar duplicados de código de barras entre tabla1 y tabla2
codigos1 = set(df1['codigo_producto'].dropna())
codigos2 = df2_long['codigo_producto'].value_counts()

# Eliminar códigos únicos entre ambas tablas
codigos_a_eliminar = codigos2[codigos2 == 1].index
df2_long = df2_long[~df2_long['codigo_producto'].isin(codigos_a_eliminar)]

# Exportar el resultado
df2_long.to_csv('tabla2_transformada.csv', index=False, encoding='utf-8')
