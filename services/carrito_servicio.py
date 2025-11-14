class CarritoServicio:

    def __init__(self, producto_servicio=None, usuario_servicio=None):
        # Import local para evitar ciclos en time of import
        from services.producto_servicio import ProductoServicio
        from services.usuario_servicio import UsuarioServicio

        self.producto_servicio = producto_servicio or ProductoServicio()
        self.usuario_servicio = usuario_servicio or UsuarioServicio()
        # carrito guarda items normalizados: {id, nombre, precio, cantidad, subtotal}
        self.carrito = []

    def agregar_item(self, producto, cantidad):
        """Agrega un producto al carrito. `producto` es el dict devuelto por el repositorio."""
        if not producto:
            return False, "Producto inválido"
        try:
            precio = float(producto.get("precio", 0))
            cantidad = int(cantidad)
            if cantidad <= 0:
                return False, "Cantidad inválida"
        except Exception:
            return False, "Precio o cantidad inválida"

        id_val = None
        if producto.get("_id") is not None:
            id_val = str(producto.get("_id"))
        elif producto.get("id"):
            id_val = str(producto.get("id"))

        item = {
            "id": id_val,
            "nombre": producto.get("nombre"),
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": precio * cantidad
        }
        self.carrito.append(item)
        return True, "Producto agregado"

    def obtener_items(self):
        """Devuelve lista de items en formato que espera la UI: `nombre`, `cantidad`, `precio`, `id`."""
        return [
            {"id": it["id"], "nombre": it["nombre"], "precio": it["precio"], "cantidad": it["cantidad"]}
            for it in self.carrito
        ]

    def obtener_total(self):
        return sum(item["subtotal"] for item in self.carrito)

    def procesar_compra(self, correo_usuario):
        if not self.carrito:
            return False, "El carrito está vacío"

        compra = {
            "items": self.carrito,
            "total": self.obtener_total()
        }

        # Registrar compra del usuario
        ok = self.usuario_servicio.registrar_compra(correo_usuario, compra)
        if not ok:
            return False, "Error registrando compra"

        # Actualizar stock (usar id guardado en cada item)
        for item in self.carrito:
            if item.get("id") is None:
                # no podemos reducir stock sin id
                continue
            self.producto_servicio.reducir_stock(item["id"], item["cantidad"])

        # Vaciar carrito
        self.carrito = []

        return True, "Compra realizada con éxito"
