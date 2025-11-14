# config/db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class BaseDatos:
    """Singleton para la conexión a MongoDB."""
    _instancia = None

    @staticmethod
    def obtener_bd():
        if BaseDatos._instancia is None:
            uri = os.getenv("MONGODB_URI") or ""
            nombre_bd = os.getenv("NOMBRE_BD") or ""

            # Normalizar y eliminar posibles comillas sobrantes en .env
            uri = uri.strip().strip('"').strip("'")
            nombre_bd = nombre_bd.strip().strip('"').strip("'")

            if not uri:
                raise ValueError("Falta MONGODB_URI en .env")
            if not nombre_bd:
                raise ValueError("Falta NOMBRE_BD en .env")

            try:
                cliente = MongoClient(uri)
                # Intentar ping rápido para detectar problemas de conexión/credenciales
                cliente.admin.command('ping')
            except Exception as e:
                raise ConnectionError(f"No se pudo conectar a MongoDB: {e}")

            BaseDatos._instancia = cliente[nombre_bd]
        return BaseDatos._instancia
