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
            uri = os.getenv("MONGODB_URI")
            nombre_bd = os.getenv("NOMBRE_BD")

            if not uri:
                raise ValueError("Falta MONGODB_URI en .env")
            if not nombre_bd:
                raise ValueError("Falta NOMBRE_BD en .env")

            cliente = MongoClient(uri)
            BaseDatos._instancia = cliente[nombre_bd]
        return BaseDatos._instancia
