# services/producto_servicio.py
from repositories.producto_repositorio import ProductoRepositorio

class ProductoServicio:
    """Servicio: reglas de negocio para productos."""

    def __init__(self):
        self.repo = ProductoRepositorio()

    def ver_todos(self):
        return self.repo.obtener_todos()

    def crear_producto(self, nombre, categoria, precio, stock):
        if not nombre or not categoria:
            return False, "Nombre y categoría son obligatorios."
        if precio <= 0:
            return False, "El precio debe ser mayor a 0."
        if stock < 0:
            return False, "El stock no puede ser negativo."

        datos = {
            "nombre": nombre,
            "categoria": categoria,
            "precio": float(precio),
            "stock": int(stock)
        }
        self.repo.crear(datos)
        return True, "Producto creado correctamente."

    def obtener_por_id(self, id_producto):
        return self.repo.obtener_por_id(id_producto)

    def disminuir_stock(self, id_producto, cantidad):
        """Intenta disminuir el stock de forma atómica. Retorna True/False."""
        return self.repo.disminuir_stock_atomico(id_producto, cantidad)

    def reducir_stock(self, id_producto, cantidad):
        """Alias por compatibilidad con la UI/otros servicios."""
        return self.disminuir_stock(id_producto, cantidad)
