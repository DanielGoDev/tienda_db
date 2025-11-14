import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto está en sys.path cuando
# ejecutamos el script desde `scripts/` (evita ModuleNotFoundError: No module named 'config')
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.db import BaseDatos


def main():
    print("Probando conexión a MongoDB...")
    try:
        bd = BaseDatos.obtener_bd()
        # bd es una instancia de pymongo.database.Database
        client = bd.client if hasattr(bd, 'client') else None
        if client:
            # comando ping
            try:
                client.admin.command('ping')
                print("Ping OK: conexión establecida con el servidor MongoDB.")
            except Exception as e:
                print(f"Error en ping al servidor MongoDB: {e}")

        try:
            colecciones = bd.list_collection_names()
            print(f"Base de datos seleccionada: {bd.name}")
            print(f"Colecciones ({len(colecciones)}): {colecciones}")
        except Exception as e:
            print(f"No se pudo listar colecciones: {e}")

    except Exception as e:
        print(f"Error obteniendo la BD: {e}")


if __name__ == '__main__':
    main()
