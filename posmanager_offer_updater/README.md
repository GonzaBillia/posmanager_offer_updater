# posmanager-offer-updater

## Version
2.3.3

El proyecto **posmanager-offer-updater** es una herramienta que permite procesar y actualizar ofertas de productos de una manera automatizada, normalizando los datos y calculando precios de ofertas. La herramienta permite leer archivos de entrada (en formatos CSV y TXT), normalizar los datos y realizar uniones entre ellos para obtener la información final necesaria para las ofertas. Además, genera un archivo de salida con los datos procesados y sin cabeceras.

## Estructura del Proyecto

La estructura de carpetas y archivos del proyecto es la siguiente:

```
posmanager-offer-updater
├── assets
│   └── favicon.ico                # Icono de la aplicación
├── config
│   ├── db_config.py               # Configuración para la conexión a la base de datos
│   └── env.py                     # Configuración del archivo .env
├── controllers
│   ├── file_controller.py         # Lógica para manejar archivos y configuraciones
│   ├── query_controller.py        # Lógica para manejar consultas y procesamiento de datos
│   └── process_controller.py      # Maneja el proceso completo llamando a las funciones necesarias
├── libs
│   ├── offer_calculator
│   │   ├── __init__.py            # Inicializa el módulo offer_calculator
│   │   └── calculator.py          # Contiene la lógica para calcular precios de oferta
│   ├── update_normalizer
│   │   ├── __init__.py            # Inicializa el módulo update_normalizer
│   │   └── normalizer.py          # Contiene la lógica para normalizar y limpiar los datos
│   ├── codebar_selector
│   │   ├── __init__.py            # Inicializa el módulo codebar_selector
│   │   └── selector.py            # Procesa códigos de barras para mapear IDProducto a código interno
│   └── orquestators
│       ├── quantio_barcodes.py    # Maneja el flujo de consulta y guardado para códigos de barras
│       ├── quantio_items.py       # Maneja el flujo de consulta y guardado para productos
│       └── quantio_categories.py  # Maneja el flujo de consulta y guardado para categorías
├── output
│   └── .exe                       # Carpeta donde se guardan el archivo ejecutable
├── queries
│   └── quantio.py                 # Lista de queries asociadas
├── ui
│   ├── components                 # Carpeta que contiene los componentes de la UI
│   ├── schema                     # Carpeta contenedora de los Widgets de la UI
│   └── threads                    # Carpeta con los hilos de procesos de UI
├── main.py                        # Archivo principal que ejecuta el procesamiento de ofertas
├── config.json                    # Archivo de configuración en formato JSON
├── README.md                      # Este archivo
├── requirements.txt               # Lista de dependencias del proyecto
└── .gitignore                     # Archivos y carpetas que no se deben incluir en el repositorio
```

## Descripción

El proyecto tiene varios módulos que realizan las siguientes funciones:

1. **offer_calculator**: Se encarga de calcular el precio final de las ofertas, aplicando cualquier regla o fórmula de cálculo necesario.
2. **update_normalizer**: Este módulo se encarga de normalizar los datos de los archivos de entrada, limpiando las columnas y asegurándose de que el formato de los datos sea consistente antes de realizar cualquier operación.
3. **codebar_selector**: Permite procesar un archivo de códigos de barras y mapear los IDProducto del archivo de salida generado por `offer_calculator` con los códigos internos utilizados por POSManager.
4. **orquestators**: Maneja el flujo de llamada a la base de datos y el guardado de consultas para códigos de barras, productos y categorías.
5. **controllers**: Aquí se encuentra la lógica para manejar archivos de entrada y salida, las consultas de la base de datos y la configuración asociada. Incluye el controlador principal del proceso.
6. **queries**: Contiene los archivos y configuraciones necesarios para realizar las consultas a la base de datos.
7. **ui**: La interfaz de usuario donde los usuarios pueden seleccionar los archivos de entrada, visualizar el progreso y resultados, y ejecutar el procesamiento de datos. También maneja los logs para facilitar el seguimiento del proceso.

El archivo `main.py` es el punto de entrada de la aplicación, donde se leen los archivos de datos (en formatos CSV y TXT), se normalizan y procesan, y finalmente se guarda el archivo de salida con los datos actualizados y sin las cabeceras.

### Funcionalidades Adicionales

1. Permite seleccionar la última fecha de modificación como filtro para los datos.
2. Incluye un proceso de optimización de etiquetas que genera un archivo optimizado para imprimir únicamente las etiquetas con cambios de precio.
3. Ofrece la opción de actualizar proveedores, departamentos y familias.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.6 o superior**
- **Dependencias del proyecto** (especificadas en `requirements.txt`)

## Instalación

### 1. Clonar el repositorio

Clona este repositorio en tu máquina local usando Git:

```bash
git clone https://github.com/GonzaBillia/posmanager-offer-updater.git
```

### 2. Crear un entorno virtual (opcional pero recomendado)

Es recomendable crear un entorno virtual para evitar conflictos con otras dependencias de proyectos diferentes:

```bash
cd posmanager-offer-updater
python3 -m venv venv
```

### 3. Activar el entorno virtual

Para activar el entorno virtual:

- En Linux/MacOS:

```bash
source venv/bin/activate
```

- En Windows:

```bash
venv\Scripts\activate
```

### 4. Instalar las dependencias

Instala las dependencias necesarias con pip:

```bash
pip install -r requirements.txt
```

## Uso

### 1. Preparar los archivos de entrada

Coloca los archivos de entrada (en formato CSV o TXT) en la ubicación deseada. Estos archivos deben contener los datos de los productos que se van a procesar, y deben cumplir con el formato esperado por el script.

### 2. Ejecutar el script

Ejecuta el archivo `main.py` para procesar los archivos de entrada y generar el archivo de salida con los datos actualizados:

```bash
python main.py
```

El script leerá los archivos de entrada, realizará las operaciones necesarias (como normalización, cálculo de precios y selección de códigos de barras) y generará un archivo de salida con los datos procesados. El archivo de salida se guardará en la carpeta `output/processed-files` con un nombre como `query-{fecha de hoy}.txt`.

### 3. Personalizar los archivos de entrada

Si necesitas personalizar los archivos de entrada, puedes ajustar las configuraciones dentro de los módulos `libs/offer_calculator/calculator.py`, `libs/update_normalizer/normalizer.py`, y `libs/codebar_selector/selector.py`, que contienen la lógica de procesamiento de los datos.

### 4. Personalizar las consultas

Si deseas personalizar las consultas realizadas a la base de datos, puedes editar los archivos en la carpeta `queries/`.

## Requerimientos

En el archivo `requirements.txt`, encontrarás las dependencias necesarias para ejecutar este proyecto. Para instalarlas, solo necesitas ejecutar:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye dependencias comunes como `pandas` para el procesamiento de datos y `numpy` para cálculos numéricos.

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b nueva-caracteristica`).
3. Realiza tus cambios y haz un commit (`git commit -am 'Añadir nueva característica'`).
4. Empuja tus cambios a tu repositorio remoto (`git push origin nueva-caracteristica`).
5. Crea un Pull Request en GitHub.
