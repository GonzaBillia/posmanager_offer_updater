from dotenv import load_dotenv
import os, sys

def init_env():
    # Ruta al archivo .env
    if getattr(sys, 'frozen', False):  # Si el script está empaquetado
        # Obtiene el directorio del ejecutable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path)

