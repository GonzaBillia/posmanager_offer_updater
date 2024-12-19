import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from ui.logs import get_logger
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
        ruta_guardado = filedialog.asksaveasfilename(
            title="Guardar archivo Items actualizado",
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt")]
        )

        if ruta_guardado:
            items_df.to_csv(ruta_guardado, index=False, header=False, sep='\t', encoding='utf-16', float_format="%.2f")  # Especificar formato decimal
            actualizar_log(f"archivo guardado correctamente")
            actualizar_log("---------- Proceso de calculo de oferta Terminado ----------")
            return True
        else:
            messagebox.showwarning("Cancelado", "La exportación fue cancelada.")
            actualizar_log("La exportación fue cancelada.")
            return False
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        actualizar_log(f"Error {e}")
        return False
