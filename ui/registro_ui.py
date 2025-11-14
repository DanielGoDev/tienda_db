# ui/registro_ui.py
import customtkinter as ctk
from tkinter import messagebox
from services.usuario_servicio import UsuarioServicio

class RegistroUI:
    def __init__(self, parent, on_volver=None):
        self.parent = parent
        self.on_volver = on_volver
        self.usuario_servicio = UsuarioServicio()

        self.parent.title("Registro - Tienda")
        self.parent.geometry("420x380")
        self.parent.resizable(False, False)

        ctk.CTkLabel(self.parent, text="Crear cuenta", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20,10))

        self.entry_nombre = ctk.CTkEntry(self.parent, width=320, placeholder_text="Nombre")
        self.entry_nombre.pack(pady=6)
        self.entry_correo = ctk.CTkEntry(self.parent, width=320, placeholder_text="Correo")
        self.entry_correo.pack(pady=6)
        self.entry_clave = ctk.CTkEntry(self.parent, width=320, placeholder_text="Contraseña", show="*")
        self.entry_clave.pack(pady=6)

        ctk.CTkButton(self.parent, text="Crear cuenta", width=200, command=self.crear_cuenta).pack(pady=(12,6))
        ctk.CTkButton(self.parent, text="Volver", width=120, fg_color=None, command=self.volver).pack()

    def crear_cuenta(self):
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        clave = self.entry_clave.get().strip()
        if not nombre or not correo or not clave:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        exito = self.usuario_servicio.registrar(nombre, correo, clave)
        if exito:
            messagebox.showinfo("OK", "Usuario creado correctamente")
            if self.on_volver:
                self.on_volver()
            else:
                self.parent.destroy()
        else:
            messagebox.showerror("Error", "Ese correo ya está registrado")

    def volver(self):
        self.parent.destroy()
        if self.on_volver:
            self.on_volver()
