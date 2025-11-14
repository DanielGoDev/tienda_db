# ui/login_ui.py
import tkinter as tk
from tkinter import messagebox
from services.usuario_servicio import UsuarioServicio

class LoginUI:
    """Ventana de Login con Tkinter."""

    def __init__(self, root, on_login_exitoso, on_abrir_registro):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")

        self.usuario_servicio = UsuarioServicio()
        self.on_login_exitoso = on_login_exitoso
        self.on_abrir_registro = on_abrir_registro

        self._crear_interfaz()

    def _crear_interfaz(self):
        tk.Label(self.root, text="TIENDA - LOGIN", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        frame.pack(pady=10)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.entrada_correo = tk.Entry(frame, width=30, font=("Arial", 12))
        self.entrada_correo.grid(row=1, column=0, pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.entrada_clave = tk.Entry(frame, width=30, show="*", font=("Arial", 12))
        self.entrada_clave.grid(row=3, column=0, pady=5)

        btn_login = tk.Button(
            frame,
            text="Iniciar Sesión",
            font=("Arial", 12, "bold"),
            width=20,
            bg="#4CAF50",
            fg="white",
            command=self.iniciar_sesion
        )
        btn_login.grid(row=4, column=0, pady=15)

        btn_registro = tk.Button(
            frame,
            text="Crear Cuenta",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=15,
            command=self.on_abrir_registro
        )
        btn_registro.grid(row=5, column=0, pady=5)

    def iniciar_sesion(self):
        correo = self.entrada_correo.get().strip()
        clave = self.entrada_clave.get().strip()

        ok, respuesta = self.usuario_servicio.iniciar_sesion(correo, clave)

        if ok:
            messagebox.showinfo("Éxito", "Inicio de sesión correcto.")
            self.on_login_exitoso(respuesta)
        else:
            messagebox.showerror("Error", respuesta)
