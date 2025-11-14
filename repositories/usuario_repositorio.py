# repositories/usuario_repositorio.py
from config.db import BaseDatos
# Usar bcrypt_sha256 evita el límite de 72 bytes del algoritmo bcrypt puro
from passlib.hash import bcrypt_sha256, bcrypt

class UsuarioRepositorio:
    def __init__(self):
        bd = BaseDatos.obtener_bd()
        self.coleccion = bd["usuarios"]

    def crear_usuario(self, nombre, correo, clave_plana):
        # Verificar que no exista
        correo_norm = correo.strip().lower()
        if self.coleccion.find_one({"correo": correo_norm}):
            return False
        clave_hash = bcrypt_sha256.hash(clave_plana)
        doc = {
            "nombre": nombre,
            "correo": correo_norm,
            "clave_hash": clave_hash,
            "historial": []
        }
        self.coleccion.insert_one(doc)
        return True

    def autenticar_usuario(self, correo, clave_plana):
        """Intenta autenticar y devuelve (True, usuario_dict) o (False, mensaje).

        Mensajes posibles: 'usuario_no_encontrado', 'sin_hash', 'clave_incorrecta', 'error_verificacion'
        """
        correo_norm = correo.strip().lower()
        usuario = self.coleccion.find_one({"correo": correo_norm})
        if not usuario:
            return False, "usuario_no_encontrado"
        clave_hash = usuario.get("clave_hash")
        if not clave_hash:
            return False, "sin_hash"

        # Intentamos verificar con bcrypt_sha256 primero, luego con bcrypt por compatibilidad
        try:
            if bcrypt_sha256.verify(clave_plana, clave_hash):
                return True, {
                    "_id": str(usuario["_id"]),
                    "nombre": usuario.get("nombre"),
                    "correo": usuario.get("correo")
                }
        except Exception:
            # ignorar y probar siguiente
            pass

        try:
            if bcrypt.verify(clave_plana, clave_hash):
                # Si la verificación pasa con `bcrypt` (hash antiguo), re-hashear
                # usando `bcrypt_sha256` para migrar el hash y evitar límites.
                try:
                    nuevo_hash = bcrypt_sha256.hash(clave_plana)
                    self.coleccion.update_one({"correo": correo_norm}, {"$set": {"clave_hash": nuevo_hash}})
                except Exception:
                    # si falla la rehash, no bloqueamos el login
                    pass

                return True, {
                    "_id": str(usuario["_id"]),
                    "nombre": usuario.get("nombre"),
                    "correo": usuario.get("correo")
                }
            else:
                return False, "clave_incorrecta"
        except Exception:
            return False, "error_verificacion"

    def registrar_compra(self, correo, compra):
        self.coleccion.update_one(
            {"correo": correo},
            {"$push": {"historial": compra}}
        )
