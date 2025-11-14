import sys
from pathlib import Path

# Asegurar ruta raíz del proyecto
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.db import BaseDatos


def detectar_tipo_hash(h):
    if not h or not isinstance(h, str):
        return 'sin_hash'
    # bcrypt-sha256 hashes suelen comenzar con $bcrypt-sha256$
    if h.startswith('$bcrypt-sha256$'):
        return 'bcrypt_sha256'
    # bcrypt clásico ($2b$ o $2a$)
    if h.startswith('$2'):
        return 'bcrypt'
    # otros (argon2, pbkdf2 etc.)
    if h.startswith('$argon2'):
        return 'argon2'
    if h.startswith('$pbkdf2'):
        return 'pbkdf2'
    return 'desconocido'


def main():
    bd = BaseDatos.obtener_bd()
    coleccion = bd['usuarios']
    cursor = coleccion.find({}, {'correo': 1, 'nombre': 1, 'clave_hash': 1})
    usuarios = list(cursor)
    if not usuarios:
        print('No hay usuarios en la colección `usuarios`.')
        return
    print(f'Usuarios encontrados: {len(usuarios)}')
    for u in usuarios:
        correo = u.get('correo')
        nombre = u.get('nombre')
        h = u.get('clave_hash')
        tipo = detectar_tipo_hash(h)
        print(f'- {correo} | {nombre} | hash: {tipo}')


if __name__ == '__main__':
    main()
