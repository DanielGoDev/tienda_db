import sys
from pathlib import Path

# Asegurar ruta raíz del proyecto
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.db import BaseDatos
from passlib.hash import bcrypt_sha256


def crear_usuario(nombre, correo, clave):
    correo_norm = correo.strip().lower()
    bd = BaseDatos.obtener_bd()
    coleccion = bd["usuarios"]

    existente = coleccion.find_one({"correo": correo_norm})
    if existente:
        print(f"El correo {correo_norm} ya está registrado")
        return False

    hash_pw = bcrypt_sha256.hash(clave)
    doc = {
        "nombre": nombre,
        "correo": correo_norm,
        "clave_hash": hash_pw,
        "historial": []
    }
    coleccion.insert_one(doc)
    print(f"Usuario creado: {correo_norm}")
    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Crear usuario en la colección 'usuarios' de la BD configurada.")
    parser.add_argument('-n', '--nombre', default='Usuario', help='Nombre del usuario')
    parser.add_argument('-e', '--email', default='daniel@correo.com', help='Correo del usuario')
    parser.add_argument('-p', '--password', default='1234', help='Contraseña (texto plano)')

    args = parser.parse_args()
    crear_usuario(args.nombre, args.email, args.password)
