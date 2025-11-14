# repositories/producto_repositorio.py
from config.db import BaseDatos
from bson import ObjectId

class ProductoRepositorio:
    """Repository: maneja CRUD de productos en MongoDB."""

    def __init__(self):
        bd = BaseDatos.obtener_bd()
        self.coleccion = bd["productos"]

    def obtener_todos(self):
        return list(self.coleccion.find())

    def obtener_por_id(self, id_producto):
        try:
            oid = ObjectId(id_producto)
        except Exception:
            return None
        return self.coleccion.find_one({"_id": oid})

    def crear(self, datos):
        return self.coleccion.insert_one(datos)

    def disminuir_stock_atomico(self, id_producto, cantidad):
        """
        Disminuye stock de forma atómica solo si stock >= cantidad.
        Retorna True si se actualizó, False si no había stock suficiente.
        """
        try:
            oid = ObjectId(id_producto)
        except Exception:
            return False

        resultado = self.coleccion.update_one(
            {"_id": oid, "stock": {"$gte": cantidad}},
            {"$inc": {"stock": -cantidad}}
        )
        return resultado.modified_count == 1
