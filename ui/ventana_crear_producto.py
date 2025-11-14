# ui/crear_producto_ui.py
import customtkinter as ctk
from tkinter import messagebox
from services.producto_servicio import ProductoServicio

class CrearProductoUI:
    def __init__(self, parent, refrescar_callback=None):
        self.parent = parent
        self.refrescar = refrescar_callback
        self.servicio = ProductoServicio()

        self.win = ctk.CTkToplevel(self.parent)
        self.win.title("Crear Producto")
        self.win.geometry("380x380")
        self.win.resizable(False, False)

        ctk.CTkLabel(self.win, text="Nuevo producto", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(12,8))

        self.e_nombre = ctk.CTkEntry(self.win, width=320, placeholder_text="Nombre")
        self.e_nombre.pack(pady=6)
        self.e_categoria = ctk.CTkEntry(self.win, width=320, placeholder_text="Categoría")
        self.e_categoria.pack(pady=6)
        self.e_precio = ctk.CTkEntry(self.win, width=320, placeholder_text="Precio")
        self.e_precio.pack(pady=6)
        self.e_stock = ctk.CTkEntry(self.win, width=320, placeholder_text="Stock")
        self.e_stock.pack(pady=6)

        ctk.CTkButton(self.win, text="Crear", width=200, command=self.crear_producto).pack(pady=(12,8))

    def crear_producto(self):
        try:
            nombre = self.e_nombre.get().strip()
            categoria = self.e_categoria.get().strip()
            precio = float(self.e_precio.get().strip())
            stock = int(self.e_stock.get().strip())
        except Exception:
            messagebox.showerror("Error", "Precio o stock inválidos")
            return

        ok, msg = self.servicio.crear_producto(nombre, categoria, precio, stock)
        if ok:
            messagebox.showinfo("OK", msg)
            self.win.destroy()
            if self.refrescar:
                self.refrescar()
        else:
            messagebox.showerror("Error", msg)
