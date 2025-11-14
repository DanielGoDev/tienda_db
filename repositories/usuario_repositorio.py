# repositories/usuario_repositorio.py
from config.db import BaseDatos
from passlib.hash import bcrypt

class UsuarioRepositorio:
    def __init__(self):
        bd = BaseDatos.obtener_bd()
        self.coleccion = bd["usuarios"]

    def crear_usuario(self, nombre, correo, clave_plana):
        # Verificar que no exista
        if self.coleccion.find_one({"correo": correo}):
            return False
        clave_hash = bcrypt.hash(clave_plana)
        doc = {
            "nombre": nombre,
            "correo": correo,
            "clave_hash": clave_hash,
            "historial": []
        }
        self.coleccion.insert_one(doc)
        return True

    def autenticar_usuario(self, correo, clave_plana):
        usuario = self.coleccion.find_one({"correo": correo})
        if not usuario:
            return None
        clave_hash = usuario.get("clave_hash")
        if not clave_hash:
            return None
        if bcrypt.verify(clave_plana, clave_hash):
            return {
                "_id": str(usuario["_id"]),
                "nombre": usuario.get("nombre"),
                "correo": usuario.get("correo")
            }
        return None

    def registrar_compra(self, correo, compra):
        self.coleccion.update_one(
            {"correo": correo},
            {"$push": {"historial": compra}}
        )
