# ui/ventana_carrito.py
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaCarrito:
    """Toplevel para ver el carrito y procesar compra."""

    def __init__(self, root, servicio_carrito, correo_usuario, refrescar_productos_callback=None):
        self.servicio = servicio_carrito
        self.correo_usuario = correo_usuario
        self.refrescar_productos = refrescar_productos_callback
        self.win = tk.Toplevel(root)
        self.win.title("Carrito")
        self.win.geometry("500x350")

        self.tree = ttk.Treeview(self.win, columns=("nombre", "cantidad", "precio"), show="headings")
        self.tree.heading("nombre", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.win, text="Comprar", command=self.comprar).pack(pady=5)
        tk.Button(self.win, text="Cerrar", command=self.win.destroy).pack()

        self.cargar_items()

    def cargar_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.servicio.obtener_items():
            self.tree.insert("", "end", values=(item["nombre"], item["cantidad"], item["precio"] * item["cantidad"]))

    def comprar(self):
        ok, msg = self.servicio.procesar_compra(self.correo_usuario)
        if ok:
            messagebox.showinfo("Compra", msg)
            self.win.destroy()
            if self.refrescar_productos:
                self.refrescar_productos()
        else:
            messagebox.showerror("Error", msg)
            self.cargar_items()
