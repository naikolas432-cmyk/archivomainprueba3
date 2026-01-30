<<<<<<< HEAD
# Backend Verano 3 - Gestión de Proyectos API

API backend construido con Django Rest Framework para la gestión de clientes, proyectos, tareas y subtareas. Implementa autenticación JWT, roles de usuario y aislamiento de datos siguiendo buenas prácticas del repositorio `vetocanti/backend-verano-3`.

## ✨ Características

- ✅ Autenticación JWT (login, refresh)
- ✅ Sistema de roles (ADMIN, CLIENT)
- ✅ Aislamiento de datos por usuario
- ✅ Cálculo automático de progreso
- ✅ Eliminación lógica de registros
- ✅ Tests automatizados incluidos
- ✅ Paginación y filtrado
- ✅ Validaciones avanzadas

## Requisitos

- Python 3.8+
- pip
- MySQL/MariaDB (opcional, SQLite por defecto)

## Instalación rápida

1. Crear y activar un entorno virtual:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Instalar dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:

   ```powershell
   Copy-Item .env.example .env
   # Editar .env con tus credenciales (opcional)
   ```

4. Migraciones y usuario administrador:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Ejecutar el servidor de desarrollo:

   ```powershell
   python manage.py runserver
   ```

## Ejecutar tests

```powershell
python manage.py test core
```

## Archivos importantes

- `manage.py`: entrada del proyecto
- `db.sqlite3`: base de datos SQLite (por defecto)
- `core/models.py`: modelos (Cliente, Proyecto, Tarea, SubTarea, Profile)
- `core/views.py`: viewsets RESTful
- `core/serializers.py`: serializadores con validaciones
- `core/permissions.py`: permisos basados en roles
- `core/signals.py`: creación automática de Profile
- `core/tests.py`: tests unitarios
- `config/settings.py`: configuración Django
- `BUENAS_PRACTICAS.md`: documentación técnica detallada

## Endpoints principales

### Autenticación

- `POST /api/auth/register/` - Registrar nuevo usuario
- `POST /api/auth/token/` - Obtener token JWT
- `POST /api/auth/token/refresh/` - Refrescar token

### Clientes (Solo Admin)

- `GET /api/clientes/` - Listar clientes
- `POST /api/clientes/` - Crear cliente
- `PUT /api/clientes/{id}/` - Actualizar cliente
- `DELETE /api/clientes/{id}/` - Eliminar cliente (desactivar)

### Proyectos

- `GET /api/proyectos/` - Listar proyectos
- `POST /api/proyectos/` - Crear proyecto
- `PUT /api/proyectos/{id}/` - Actualizar proyecto
- `DELETE /api/proyectos/{id}/` - Eliminar proyecto

### Tareas

- `GET /api/tareas/` - Listar tareas
- `POST /api/tareas/` - Crear tarea
- `PUT /api/tareas/{id}/` - Actualizar tarea
- `DELETE /api/tareas/{id}/` - Eliminar tarea

### SubTareas

- `GET /api/subtareas/` - Listar subtareas
- `POST /api/subtareas/` - Crear subtarea
- `PUT /api/subtareas/{id}/` - Actualizar subtarea
- `DELETE /api/subtareas/{id}/` - Eliminar subtarea

## Estructura de Datos

```
Profile (role: ADMIN/CLIENT)
    ↓
Usuario ← Proyecto
            ↓
        Cliente
            ↓
         Tarea
            ↓
        SubTarea
```

## Autenticación JWT

### Registrar usuario:
```bash
POST /api/auth/register/
{
  "username": "admin1",
  "password": "strongpass123",
  "email": "admin@example.com",
  "role": "ADMIN"
}
```

### Obtener token:
```bash
POST /api/auth/token/
{
  "username": "admin1",
  "password": "strongpass123"
}
```

### Usar el token:
```bash
Authorization: Bearer <tu_token_aqui>
```

## Sistema de Roles

### ADMIN
- ✅ CRUD completo en todos los recursos
- ✅ Acceso a todos los datos
- ✅ Ver panel de administración

### CLIENT
- ✅ Lectura de sus propios proyectos
- ✅ Lectura de tareas y subtareas asociadas
- ❌ No puede crear, actualizar ni eliminar

## Notas importantes

- Ajusta las variables en `.env` según tu entorno
- La base de datos por defecto es SQLite (db.sqlite3)
- Para MySQL, configura variables en `.env` y Django Auto-detecta la BD
- Todos los endpoints requieren autenticación JWT (excepto `/api/auth/register/` y `/api/auth/token/`)
- El aislamiento de datos se garantiza mediante permisos y `get_queryset()`
- Consulta `BUENAS_PRACTICAS.md` para documentación técnica completa

- `DELETE /api/clientes/{id}/` - Eliminar cliente (desactivar)

- `GET /api/proyectos/` - Listar proyectos
- `POST /api/proyectos/` - Crear proyecto
- `PUT /api/proyectos/{id}/` - Actualizar proyecto
- `DELETE /api/proyectos/{id}/` - Eliminar proyecto

- `GET /api/tareas/` - Listar tareas
- `POST /api/tareas/` - Crear tarea
- `PUT /api/tareas/{id}/` - Actualizar tarea
- `DELETE /api/tareas/{id}/` - Eliminar tarea

- `GET /api/subtareas/` - Listar subtareas
- `POST /api/subtareas/` - Crear subtarea
- `PUT /api/subtareas/{id}/` - Actualizar subtarea
- `DELETE /api/subtareas/{id}/` - Eliminar subtarea

## Notas

- Ajusta las variables de configuración en `config/settings.py` según tu entorno.
- Los usuarios con rol ADMIN tienen acceso completo.
- Los usuarios con rol CLIENT solo pueden ver sus propios datos.


Tarea: Unidad de trabajo dentro de un proyecto.

SubTarea: Nivel de detalle técnico final.

🧪 Pruebas de API
Se incluye una colección de Postman para probar los siguientes casos:

Obtención de Token (POST /api/token/)

Creación de Clientes y Proyectos (POST)

Validación de rangos de progreso (Error 400)

Eliminación lógica de clientes (DELETE)
=======
# archivomainprueba3
>>>>>>> f7c9ba3487bb74ea4fe0a3c5cfbceecd92850fa2
