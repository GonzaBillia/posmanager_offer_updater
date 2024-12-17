# Posmanager Update Normalizer

## Versión
1.0.1

## Descripción
El programa **Posmanager Update Normalizer** está diseñado para facilitar la actualización de listas de productos en Posmanager, asegurando que:

- Los códigos internos (‘codigoInterno’) sean asignados correctamente.
- No se generen códigos duplicados.
- Se evite la modificación incorrecta de códigos existentes.

### Funcionalidad principal

El programa toma dos archivos como entrada:

1. **Lista de actualización**: Un archivo generado a partir de una consulta a la base de datos de Quantio.
2. **Lista completa de productos de Posmanager**: Contiene todos los productos registrados actualmente en el sistema Posmanager.

El programa genera un tercer archivo de salida en formato `.csv` que:

- Conserva el formato del archivo de actualización.
- Incluye los códigos correctos de Posmanager en la columna `codigoInterno`.
- Asigna nuevos códigos únicos cuando sea necesario.

### Validaciones
- Los nuevos códigos generados no se duplican con los ya existentes en la lista de productos de Posmanager.
- Los códigos existentes se respetan y no se sobrescriben.

---

## Requisitos de instalación

### Prerrequisitos
- **Python 3.10 o superior**
- Dependencias de Python:
  - `pandas`
  - `tkinter`

### Instalación
1. Clona o descarga el repositorio del programa.
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_DIRECTORIO>
   ```
2. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install pandas
   ```
   La librería `tkinter` está incluida en la mayoría de las distribuciones de Python por defecto. Si no está disponible, consulta la documentación específica para tu sistema operativo.

---

## Uso del programa

### Ejecución
1. Ejecuta el programa con Python:
   ```bash
   python app.py
   ```
2. Selecciona los archivos de entrada:
   - Primero, selecciona el archivo de **lista de actualización** (formato CSV delimitado por tabulaciones).
   - Luego, selecciona el archivo de **lista completa de productos de Posmanager** (formato TXT delimitado por comas).
3. Selecciona el nombre y ubicación del archivo de salida.
   - El archivo generado estará en formato `.csv` o `.xlsx`, según la opción que elijas.

### Formato de salida
- El archivo resultante incluye todas las columnas del archivo de actualización original, con los códigos de Posmanager en la columna `codigoInterno`.
- Si el código interno está vacío o es inválido, el programa asigna un nuevo código único validado.
- La cabecera de la columna `codigoInterno` está en blanco, como se especificó.

---

## Notas adicionales
- Asegúrate de que los archivos de entrada estén en el formato correcto:
  - **Lista de actualización**: CSV delimitado por tabulaciones.
  - **Lista completa de productos de Posmanager**: TXT delimitado por comas.
- Si experimentas problemas de codificación, verifica que los archivos estén guardados con la codificación `latin1`.

---

