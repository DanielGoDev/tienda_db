# ui/tienda_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.producto_servicio import ProductoServicio
from services.carrito_servicio import CarritoServicio
from ui.ventana_crear_producto import CrearProductoUI

class TiendaUI:
    def __init__(self, usuario):
        self.usuario = usuario
        self.servicio_producto = ProductoServicio()
        self.servicio_carrito = CarritoServicio()

        self.root = tk.Toplevel()
        self.root.title("Tienda")
        self.root.geometry("900x600")

        # Productos
        tk.Label(self.root, text=f"Tienda - Usuario: {self.usuario['nombre']}",
                 font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        frame_prod = tk.Frame(self.root)
        frame_prod.pack(fill="both", expand=False, padx=10, pady=5)

        tk.Label(frame_prod, text="Productos disponibles",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        self.tree = ttk.Treeview(
            frame_prod,
            columns=("id", "nombre", "categoria", "precio", "stock"),
            show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        self.tree.column("id", width=0)

        self.tree.pack(fill="both", expand=True)

        # Controles
        cont = tk.Frame(self.root)
        cont.pack(fill="x", padx=10, pady=10)

        tk.Label(cont, text="Cantidad:").pack(side="left")
        self.entry_cantidad = tk.Entry(cont, width=6)
        self.entry_cantidad.pack(side="left", padx=5)

        tk.Button(cont, text="Agregar al carrito",
                  command=self.agregar_seleccion).pack(side="left", padx=5)

        tk.Button(cont, text="Crear producto",
                  command=self.abrir_crear_producto).pack(side="left", padx=5)

        tk.Button(cont, text="Refrescar", command=self.cargar_productos).pack(side="left", padx=5)

        tk.Button(cont, text="Cerrar sesión", command=self.cerrar_sesion).pack(side="right", padx=5)

        # Carrito
        frame_cart = tk.Frame(self.root)
        frame_cart.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame_cart, text="Carrito",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        self.tree_cart = ttk.Treeview(
            frame_cart,
            columns=("nombre", "cantidad", "subtotal"),
            show="headings"
        )
        self.tree_cart.heading("nombre", text="Producto")
        self.tree_cart.heading("cantidad", text="Cantidad")
        self.tree_cart.heading("subtotal", text="Subtotal")

        self.tree_cart.pack(fill="both", expand=True)

        # Total + Comprar
        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", padx=10, pady=10)

        self.lbl_total = tk.Label(bottom, text="Total: $0",
                                  font=("Arial", 12, "bold"))
        self.lbl_total.pack(side="left")

        tk.Button(bottom, text="Realizar compra",
                  bg="green", fg="white",
                  command=self.realizar_compra).pack(side="right")

        # Cargar datos
        self.cargar_productos()
        self.cargar_carrito()

        self.root.mainloop()

    # -------------------------------------------------------------

    def cargar_productos(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.servicio_producto.ver_todos():
            id_str = str(p["_id"])
            self.tree.insert("", "end", iid=id_str,
                             values=(id_str, p["nombre"],
                                     p.get("categoria", ""),
                                     p.get("precio", 0),
                                     p.get("stock", 0)))

    # -------------------------------------------------------------

    def agregar_seleccion(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un producto.")
            return

        id_sel = seleccionado[0]

        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        producto = self.servicio_producto.obtener_por_id(id_sel)
        ok, msg = self.servicio_carrito.agregar_item(producto, cantidad)

        if ok:
            self.cargar_carrito()
            messagebox.showinfo("Carrito", msg)
        else:
            messagebox.showerror("Error", msg)

    # -------------------------------------------------------------

    def cargar_carrito(self):
        self.tree_cart.delete(*self.tree_cart.get_children())
        total = 0

        for it in self.servicio_carrito.obtener_items():
            subtotal = it["precio"] * it["cantidad"]
            total += subtotal
            self.tree_cart.insert("", "end",
                                  values=(it["nombre"], it["cantidad"], subtotal))

        self.lbl_total.config(text=f"Total: ${total}")

    # -------------------------------------------------------------

    def realizar_compra(self):
        ok, msg = self.servicio_carrito.procesar_compra(self.usuario["correo"])
        if ok:
            messagebox.showinfo("Compra", msg)
            self.cargar_productos()
            self.cargar_carrito()
        else:
            messagebox.showerror("Error", msg)

    # -------------------------------------------------------------

    def abrir_crear_producto(self):
        CrearProductoUI(self.root, refrescar_callback=self.cargar_productos)

    # -------------------------------------------------------------

    def cerrar_sesion(self):
        self.root.destroy()
        from ui.login_ui import LoginUI
        LoginUI().run()
