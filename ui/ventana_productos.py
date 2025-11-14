# ui/ventana_productos.py
import tkinter as tk
from tkinter import ttk

class VentanaProductos:

    def __init__(self, root, servicio):
        self.servicio = servicio

        self.win = tk.Toplevel(root)
        self.win.title("Productos Disponibles")
        self.win.geometry("500x400")

        self.tabla = ttk.Treeview(self.win, columns=("nombre", "categoria", "precio", "stock"), show="headings")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        self.tabla.pack(fill="both", expand=True)

        self.cargar_productos()

    def cargar_productos(self):
        productos = self.servicio.ver_todos()

        for p in productos:
            self.tabla.insert("", "end", values=(p["nombre"], p["categoria"], p["precio"], p["stock"]))
