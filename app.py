import tkinter as tk
from ui.login_ui import LoginUI
from ui.registro_ui import RegistroUI
from ui.tienda_ui import TiendaUI

def abrir_login():
    root = tk.Tk()

    def login_exitoso(usuario):
        root.destroy()
        TiendaUI(usuario)  # ← NO necesita root

    def abrir_registro():
        root.destroy()
        abrir_ventana_registro()

    LoginUI(root, login_exitoso, abrir_registro)
    root.mainloop()

def abrir_ventana_registro():
    root = tk.Tk()

    def registro_exitoso():
        root.destroy()
        abrir_login()

    RegistroUI(root, registro_exitoso)
    root.mainloop()

if __name__ == "__main__":
    abrir_login()
