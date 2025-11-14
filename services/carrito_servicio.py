class CarritoServicio:

    def __init__(self, producto_servicio, usuario_servicio):
        self.producto_servicio = producto_servicio
        self.usuario_servicio = usuario_servicio
        self.carrito = []

    def agregar(self, producto, cantidad):
        self.carrito.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": producto["precio"] * cantidad
        })
        return True, "Producto agregado"

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

        # Actualizar stock
        for item in self.carrito:
            self.producto_servicio.reducir_stock(
                item["producto"]["id"],
                item["cantidad"]
            )

        # Vaciar carrito
        self.carrito = []

        return True, "Compra realizada con éxito"
