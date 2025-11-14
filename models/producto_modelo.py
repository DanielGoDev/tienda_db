# models/producto_modelo.py

class Producto:
    """Modelo que define un producto dentro de la tienda."""
    def __init__(self, nombre, categoria, precio, stock):
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
