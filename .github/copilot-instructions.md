<!-- .github/copilot-instructions.md -->

# Repo guidance for AI coding agents

Purpose: help an AI coding agent get productive quickly in this repository (`tienda_db`). Focus is on the actual code layout, conventions, runtime prerequisites, and notable inconsistencies to avoid making incorrect edits.

1. Big picture

- UI: `ui/` — Tkinter (and `customtkinter`) windows and view logic (entry points: `app.py`, `ui/login_ui.py`, `ui/tienda_ui.py`). The UI calls into services directly.
- Services: `services/` — business rules and orchestrations. Services are intended to use repository classes to read/write data.
- Repositories: `repositories/` — direct MongoDB access via `config/db.py` singleton. Use `bson.ObjectId` for `_id` conversions and atomic updates (see `producto_repositorio.disminuir_stock_atomico`).
- Models: `models/` — lightweight Python objects used to structure domain data (simple classes, no ORM).
- Config: `config/db.py` — single source for Mongo connection. Requires `.env` keys: `MONGODB_URI` and `NOMBRE_BD`.

2. Run / debug workflow (what actually works)

- Ensure a virtual environment is active (repo contains `venv/`). In PowerShell:

```
venv\Scripts\Activate.ps1
pip install -r requirements.txt  # if you add one
python app.py
```

- Required environment variables (in `.env`): `MONGODB_URI`, `NOMBRE_BD`. `config/db.py` will raise ValueError if missing.
- Key dependencies (inferred from imports): `pymongo`, `python-dotenv`, `passlib[bcrypt]`, `customtkinter`. If using `mongodb+srv` also ensure `dnspython` is available.

3. Project-specific patterns and examples

- DB: `config/BaseDatos.obtener_bd()` returns a `pymongo` `Database` instance. Repositories call `bd["coleccion"]`. Example: `repositories/usuario_repositorio.py` uses `self.coleccion = bd["usuarios"]` and stores `clave_hash` with `passlib.hash.bcrypt`.
- ObjectId handling: repository methods convert string ids using `bson.ObjectId` and return `None` on invalid ids (see `producto_repositorio.obtener_por_id`). When inserting, Mongo returns an InsertOneResult — service layer should convert `_id` to `str` before sending to UI.
- Atomic updates: prefer Mongo queries that use conditional updates (see `disminuir_stock_atomico`) to avoid race conditions.
- Models are plain classes (example: `models/usuario_modelo.py`). Repositories return dictionaries from Mongo; services may construct model instances if needed.

4. Conventions and language

- Code uses Spanish identifiers (`usuario`, `correo`, `clave`, `carrito`, etc.). Keep new identifiers consistent with Spanish naming.
- Prefer repository method names as the source-of-truth for DB behaviour (`obtener_todos`, `obtener_por_id`, `crear`, `disminuir_stock_atomico`). When changing service or UI code, align method names to repository APIs.

5. Known inconsistencies (important to check before editing)

- There are multiple mismatches between layers — do not assume method names across files are consistent. Examples found while scanning:
  - `services/usuario_servicio.py` currently imports `from db import db` and uses `BD()` — this does not match `config/db.py` (`BaseDatos`). Treat `repositories/*` and `config/db.py` as canonical for DB behavior.
  - `ui/tienda_ui.py` calls `CarritoServicio()` with no args and expects methods like `agregar_item`, `obtener_items`, and `reducir_stock` on services, but `services/carrito_servicio.py` and `services/producto_servicio.py` expose different method names (`agregar`, `obtener_total`, `procesar_compra`, `disminuir_stock`). Before edits, run the app or open the file pair and reconcile names.

6. Editing guidance for AI agents

- Start from repository and repository method names when adding or changing persistence logic.
- If you change a service API, update all call sites in `ui/` and other services in the same PR — search the codebase for the symbol and update callers.
- Keep UI logic free of DB details. Do not add Mongo access inside `ui/` files; instead extend a service method and call it from the UI.
- When altering DB schema (document fields), update both the repository code and any code that reads those fields (UI and services). Example fields: `usuarios` documents use `nombre`, `correo`, `clave_hash`, `historial`.

7. Examples the agent can use directly

- Authenticate user (pattern used in `repositories/usuario_repositorio.py`):
  - find document by `correo`
  - verify `clave_plana` with `passlib.hash.bcrypt.verify`
  - return a dict with stringified `_id` and `nombre`/`correo` for UI consumption
- Decrease product stock atomically (pattern used in `repositories/producto_repositorio.py`):
  - `update_one({"_id": oid, "stock": {"$gte": cantidad}}, {"$inc": {"stock": -cantidad}})`

8. When adding tests or checks

- There are no tests found in the repo. If adding tests, mock `config.BaseDatos.obtener_bd()` to return an in-memory or stubbed collection and avoid requiring a live Mongo instance.

9. Where to look first when something breaks

- `app.py` — app entrypoint and window flow
- `config/db.py` — Mongo connection and required env
- `repositories/*` — DB queries and object id handling
- `services/*` — business rules and method names that the UI expects
- `ui/*` — UI entry points and calls into services; common failure: method name mismatch or expecting dict vs model

10. Ask for feedback

- If a section is unclear or you want more examples (e.g., expected document shapes for `productos` and `usuarios`), tell me which files you want me to open and I will extract concrete JSON examples.

---

If you want, I can now: (A) create a `requirements.txt` based on imports, (B) reconcile the mismatched service/UI method names into a consistent API, or (C) generate sample `.env.example` with the required variables. Which should I do next?
