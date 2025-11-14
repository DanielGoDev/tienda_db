from db import db

class UsuarioServicio:
    def __init__(self):
        self.db = BD()

    def registrar_usuario(self, nombre, correo, password):
        return self.db.insertar_usuario(nombre, correo, password)

    def obtener_usuario(self, correo, password):
        return self.db.obtener_usuario(correo, password)

    # =============================================
    #  NUEVO MÉTODO → evitar error y registrar compras
    # =============================================
    def registrar_compra(self, correo_usuario, compra):
        """
        compra = {
            "items": [...],
            "total": 12345
        }
        """
        return self.db.guardar_compra(correo_usuario, compra)
