import pandas as pd
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from ui.components.logs import get_logger
import unicodedata

# Obtener la función para actualizar logs
actualizar_log = get_logger()

def normalizar_texto(texto):
    if isinstance(texto, str):
        return ''.join(
            c for c in unicodedata.normalize('NFKD', texto)
            if not unicodedata.combining(c)
        )
    return texto

def calcular_ofertas(output_file, archivo_propuesta):

    try:
        # Cargar archivos Excel con manejo de errores
        try:
            items_df = pd.read_csv(output_file)
            propuesta_df = pd.read_excel(archivo_propuesta)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los archivos: {e}")
            actualizar_log("Error al leer los archivos para calcular")
            return

        # Normalizar texto en todas las columnas
        items_df = items_df.applymap(normalizar_texto)
        propuesta_df = propuesta_df.applymap(normalizar_texto)

        # Limpiar y convertir la columna de precios a float
        items_df[items_df.columns[8]] = items_df[items_df.columns[8]].replace({',': '.'}, regex=True).astype(float)

        # Verificar existencia de columnas
        if "IDProducto" not in items_df.columns or propuesta_df.columns[0] != "Id Quantio":
            messagebox.showerror("Error", "¡Faltan las columnas IDProducto o Id Quantio o su nombre ha cambiado")
            actualizar_log("Faltan las columnas IDProducto o Id Quantio o su nombre ha cambiado. Revisalo y vuelve a intentarlo")
            actualizar_log(f"Columnas del archivo normalizado: [ {items_df} ]")
            actualizar_log(f"Columnas del archivo de propuesta: [ {propuesta_df} ]")
            return

        # Asegurar que la columna Precio_de_Oferta_Etiquetas esté en la posición 23
        if "Precio_de_Oferta_Etiquetas" not in items_df.columns:
            messagebox.showerror("Error", "¡La columna Precio_de_Oferta_Etiquetas no existe en el archivo Items!")
            actualizar_log("¡La columna Precio_de_Oferta_Etiquetas no existe en el archivo Items!")
            actualizar_log(f"Columnas del archivo normalizado: [ {items_df} ]")
            return

        def calcular_precio_final(id_producto, precio_final):
            try:
                # Asegurarse de que precio_final sea un número flotante
                precio_final = float(precio_final)  # Convertir precio_final a float

                # Buscar el descuento correspondiente en el archivo de propuesta
                if id_producto in propuesta_df.iloc[:, 0].values:
                    descuento_str = propuesta_df.loc[propuesta_df.iloc[:, 0] == id_producto, propuesta_df.columns[1]].values[0]
                    
                    # Convertir el descuento a float, manejando posibles errores
                    descuento = float(descuento_str)
                    
                    # Verificar si el descuento es un porcentaje o un precio fijo
                    if descuento <= 1:  # Descuento como porcentaje
                        return precio_final * (1 - descuento), True
                    else:  # Precio fijo
                        return descuento, True
                return "", False  # Si no se encuentra el producto, devolver vacío
            except ValueError:
                # Manejar si no se puede convertir el descuento o el precio a un número flotante
                actualizar_log(f"Error al convertir el descuento de {id_producto} o el precio a flotante.")
                return "", False

        # Calcular precios y agregar indicador de descuento
        descuentos = items_df.apply(
            lambda row: calcular_precio_final(row["IDProducto"], row[items_df.columns[8]]), axis=1
        )
        items_df.iloc[:, 23] = [precio for precio, _ in descuentos]

        # Verificar si la columna de índice 35 existe, y agregarla si no tiene encabezado
        if len(items_df.columns) <= 35:
            items_df.insert(35, 'Es Oferta', "")  # Agregar una nueva columna llamada 'Es Oferta' en el índice 35

        items_df.iloc[:, 35] = ["S" if descuento else "N" for _, descuento in descuentos]

        # Reemplazar comas por puntos en las columnas y convertirlas a numérico
        items_df.iloc[:, [8, 22, 23, 24]] = items_df.iloc[:, [8, 22, 23, 24]].replace(",", ".", regex=True)
        items_df.iloc[:, [8, 22, 23, 24]] = items_df.iloc[:, [8, 22, 23, 24]].apply(pd.to_numeric, errors='coerce')

        # Rellenar valores NaN con 0 (opcional)
        items_df.iloc[:, [8, 22, 23, 24]] = items_df.iloc[:, [8, 22, 23, 24]].fillna(0)



        # Exportar archivo actualizado como TXT Unicode
        # Definir la ruta del directorio de salida
        output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\processed-files\\calculated-items')

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Obtener la fecha de hoy
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')

        # Crear el nombre de archivo con la fecha de hoy
        output_file = os.path.join(output_dir, f"calc-items-{fecha_hoy}.txt")

        # Guardar el resultado en el archivo
        items_df.to_csv(output_file, index=False, header=False, sep='\t', encoding='utf-16', float_format="%.2f")

        # Registrar la acción
        actualizar_log(f"Archivo guardado correctamente en: {output_file}")
        actualizar_log("---------- Proceso de cálculo de oferta Terminado ----------")

        return True, output_file
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        actualizar_log(f"Error {e}")
        return False

def optimizar_lectoras(output_file, first_filter):
    try:
        # Leer archivo
        df = pd.read_csv(output_file, sep='\t', encoding='utf-16', header=None)

        # Validar que el DataFrame no esté vacío
        if df.empty:
            raise ValueError("El archivo leído está vacío o no contiene datos válidos.")

        # Verificar que las columnas necesarias existen
        required_columns = [23, 22, 8]
        if not all(col in df.columns for col in required_columns):
            raise KeyError(f"Las columnas {required_columns} no se encuentran en el archivo.")

        # Asegurar que las columnas sean tratadas como cadenas
        df[23] = df[23].astype(str)
        df[22] = df[22].astype(str)
        df[8] = df[8].astype(str)

        # Condición: filas donde precio_oferta != '0'
        condition = df[23] != '0.0'

        # Cambiar solo las filas que cumplen la condición, preservando valores originales en las demás
        df[22] = df[22].where(~condition, df[8])  # Copiar precio_final a ultimo_precio solo si la condición es True
        df[8] = df[8].where(~condition, df[23])  # Copiar precio_oferta a precio_final solo si la condición es True


        # Crear directorio de salida si no existe
        output_dir = os.path.expanduser('~\\Documents\\PM-offer-updater\\processed-files\\calculated-items')
        os.makedirs(output_dir, exist_ok=True)

        # Crear el nombre de archivo de salida
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        
        if first_filter:
            output_path = os.path.join(output_dir, f"calc-items-{fecha_hoy}.txt")
        else:
            output_path = os.path.join(output_dir, f"calc-items-opt-{fecha_hoy}.txt")

        # Guardar el resultado en el archivo
        df.to_csv(output_path, index=False, header=False, sep='\t', encoding='utf-16', float_format="%.2f")

        # Registrar la acción
        actualizar_log(f"Archivo guardado correctamente en: {output_path}")
        actualizar_log("---------- Proceso de optimizacion de etiquetas Terminado ----------")

        return True

    except Exception as e:
        actualizar_log(f"Error inesperado al optimizar columnas: {str(e)}")
        return False