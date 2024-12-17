import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import unicodedata

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
            return

        # Normalizar texto en todas las columnas
        items_df = items_df.applymap(normalizar_texto)
        propuesta_df = propuesta_df.applymap(normalizar_texto)

        # Verificar existencia de columnas
        if "IDProducto" not in items_df.columns or propuesta_df.columns[0] != "codigo_ERP":
            messagebox.showerror("Error", "¡Faltan las columnas IDProducto o codigo_ERP!")
            return

        # Asegurar que la columna Precio_de_Oferta_Etiquetas esté en la posición 23
        if "Precio_de_Oferta_Etiquetas" not in items_df.columns:
            messagebox.showerror("Error", "¡La columna Precio_de_Oferta_Etiquetas no existe en el archivo Items!")
            return

        # Actualizar la columna en la posición 23 con el cálculo correspondiente
        def calcular_precio_final(id_producto, precio_final):
            if id_producto in propuesta_df.iloc[:, 0].values:
                descuento = propuesta_df.loc[propuesta_df.iloc[:, 0] == id_producto, propuesta_df.columns[1]].values[0]
                if descuento <= 1:  # Descuento como porcentaje
                    return precio_final * (1 - descuento), True
                else:  # Precio fijo
                    return descuento, True
            return "", False

        # Calcular precios y agregar indicador de descuento
        descuentos = items_df.apply(
            lambda row: calcular_precio_final(row["IDProducto"], row[items_df.columns[8]]), axis=1
        )
        items_df.iloc[:, 23] = [precio for precio, _ in descuentos]

        # Verificar si la columna de índice 35 existe, y agregarla si no tiene encabezado
        if len(items_df.columns) <= 35:
            items_df.insert(35, 'Descuento', "")  # Agregar una nueva columna llamada 'Descuento' en el índice 35

        items_df.iloc[:, 35] = ["S" if descuento else "N" for _, descuento in descuentos]

        # Convertir las columnas 8, 23 y 24 al formato adecuado
        items_df.iloc[:, [8, 22, 23]] = items_df.iloc[:, [8, 22, 23]].apply(pd.to_numeric, errors='coerce')
        items_df.iloc[:, [8, 22, 23]] = items_df.iloc[:, [8, 22, 23]].fillna(0)  # Opcional: Manejo de NaN

        # Exportar archivo actualizado como TXT Unicode
        ruta_guardado = filedialog.asksaveasfilename(
            title="Guardar archivo Items actualizado",
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt")]
        )

        if ruta_guardado:
            items_df.to_csv(ruta_guardado, index=False, sep='\t', encoding='utf-16', float_format="%.2f")  # Especificar formato decimal
            messagebox.showinfo("Éxito", "¡Archivo guardado exitosamente!")
        else:
            messagebox.showwarning("Cancelado", "La exportación fue cancelada.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
