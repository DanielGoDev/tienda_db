# models/usuario_modelo.py

class Usuario:
    """Modelo de un usuario del sistema."""
    def __init__(self, nombre_usuario, contraseña):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.carrito = []
        self.historial = []
