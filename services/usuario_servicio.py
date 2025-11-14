from repositories.usuario_repositorio import UsuarioRepositorio


class UsuarioServicio:
    """Servicio de usuario: adapta el repositorio al API que espera la UI.

    La UI espera métodos `registrar(nombre, correo, clave)`,
    `iniciar_sesion(correo, clave)` y `registrar_compra(correo, compra)`.
    """

    def __init__(self):
        self.repo = UsuarioRepositorio()

    def registrar(self, nombre, correo, clave):
        """Registra un nuevo usuario. Retorna True si se creó, False si el correo ya existe."""
        correo_norm = correo.strip().lower()
        return self.repo.crear_usuario(nombre, correo_norm, clave)

    def iniciar_sesion(self, correo, clave):
        """Intenta autenticar al usuario.

        Retorna (True, usuario_dict) si ok, o (False, mensaje) si falla.
        """
        correo_norm = correo.strip().lower()
        ok, result = self.repo.autenticar_usuario(correo_norm, clave)
        if ok:
            return True, result
        # Mapear mensajes internos a mensajes para UI
        if result == "usuario_no_encontrado":
            return False, "Usuario no encontrado"
        if result == "sin_hash":
            return False, "Cuenta inválida (sin hash)"
        if result == "clave_incorrecta":
            return False, "Credenciales inválidas"
        if result == "error_verificacion":
            return False, "Error verificando credenciales"
        return False, "Credenciales inválidas"

    def registrar_compra(self, correo_usuario, compra):
        """Registra la compra en el historial del usuario.

        Retorna True si la operación fue enviada al repositorio.
        (El repositorio no devuelve un valor explícito en la implementación actual.)
        """
        self.repo.registrar_compra(correo_usuario, compra)
        return True
