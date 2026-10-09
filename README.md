# TechGear API RESTful - OCI Deployment

API RESTful desarrollada con **Python** y **Flask**, desplegada en una máquina virtual de **Oracle Cloud Infrastructure (OCI)** y conectada a una base de datos **MariaDB**.

---

## 🌐 Información de Despliegue
* **Base URL:** `http://40.233.3.52:5000`
* **Base de Datos:** MariaDB (`techgear_db`)
* **Colección de Postman:** Incluida en este repositorio (`TechGear_API_OCI.postman_collection.json`)

---

## 📌 Tabla de Endpoints y Métodos HTTP

| Módulo | Método HTTP | Ruta / Endpoint | Descripción | Body (JSON) / Params | Código Respuesta |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Productos** | `GET` | `/api/v1/producto` | Obtener todos los productos | N/A | `200 OK` |
| **Productos** | `POST` | `/api/v1/producto` | Registrar un nuevo producto | `{ "nombre": "...", "categoria": "...", "precio": 0.0, "stock": 0, "descripcion": "..." }` | `201 Created` |
| **Productos** | `GET` | `/api/v1/producto/<id>` | Obtener producto por ID | Parámetro `id` en URL | `200 OK` / `404` |
| **Productos** | `PUT` | `/api/v1/producto/<id>` | Actualizar producto por ID | `{ "nombre": "...", "categoria": "...", "precio": 0.0, "stock": 0, "descripcion": "..." }` | `200 OK` |
| **Productos** | `DELETE` | `/api/v1/producto/<id>` | Eliminar producto por ID | Parámetro `id` en URL | `200 OK` |
| **Clientes** | `GET` | `/api/v1/clientes` | Obtener todos los clientes | N/A | `200 OK` |
| **Clientes** | `POST` | `/api/v1/clientes` | Registrar un nuevo cliente | `{ "nombre": "...", "apellido": "...", "email": "...", "telefono": "..." }` | `201 Created` |
| **Clientes** | `GET` | `/api/v1/clientes/<id>` | Obtener cliente por ID | Parámetro `id` en URL | `200 OK` / `404` |
| **Clientes** | `PUT` | `/api/v1/clientes/<id>` | Actualizar cliente por ID | `{ "nombre": "...", "apellido": "...", "email": "...", "telefono": "..." }` | `200 OK` |
| **Clientes** | `DELETE` | `/api/v1/clientes/<id>` | Eliminar cliente por ID | Parámetro `id` en URL | `200 OK` |
| **Direcciones (1:N)** | `POST` | `/api/v1/clientes/direcciones` | Asociar dirección a un cliente | `{ "cliente_id": 1, "calle_numero": "...", "colonia": "...", "ciudad": "...", "codigo_postal": "..." }` | `201 Created` / `400` |

---

## 🛠️ Estructura del Proyecto
```text
tienda_perifericos/
├── app.py
├── db.py
├── TechGear_API_OCI.postman_collection.json
├── modulos/
│   ├── __init__.py
│   ├── clientes.py
│   └── productos.py
└── templates/
    └── index.html
