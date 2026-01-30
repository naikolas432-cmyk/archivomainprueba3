# Documentación del Proyecto - API RESTful Gestión de Proyectos

## 1. Modelo Relacional

### Diagrama de Base de Datos

```
┌─────────────────┐
│    Cliente      │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ email (UNIQUE)  │
│ empresa         │
│ activo          │
│ fecha_creacion  │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│   Proyecto      │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ descripcion     │
│ estado          │
│ progreso        │
│ cliente_id (FK) │
│ fecha_inicio    │
│ fecha_entrega   │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│     Tarea       │
├─────────────────┤
│ id (PK)         │
│ titulo          │
│ descripcion     │
│ estado          │
│ progreso        │
│ proyecto_id(FK) │
│ fecha_creacion  │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│   SubTarea      │
├─────────────────┤
│ id (PK)         │
│ titulo          │
│ completada      │
│ tarea_id (FK)   │
│ fecha_creacion  │
└─────────────────┘
```

### Relaciones

- **Cliente → Proyecto**: 1:N (Un cliente puede tener múltiples proyectos)
- **Proyecto → Tarea**: 1:N (Un proyecto puede tener múltiples tareas)
- **Tarea → SubTarea**: 1:N (Una tarea puede tener múltiples subtareas)

### Restricciones

- `Cliente.email`: UNIQUE (no se permiten emails duplicados)
- `Proyecto.progreso`, `Tarea.progreso`: Validación entre 0 y 100
- `Proyecto.fecha_entrega` debe ser posterior a `fecha_inicio`
- `Cliente.activo`: Implementa eliminación lógica

## 2. Autenticación JWT

### ¿Qué es JWT?

JSON Web Token (JWT) es un estándar abierto (RFC 7519) que define una forma compacta y autónoma de transmitir información de manera segura entre partes como un objeto JSON. Esta información puede ser verificada y confiable porque está firmada digitalmente.

### Estructura de un JWT

Un JWT consta de tres partes separadas por puntos (.):

```
xxxxx.yyyyy.zzzzz
```

1. **Header (Cabecera)**: Contiene el tipo de token y el algoritmo de hash
   ```json
   {
     "alg": "HS256",
     "typ": "JWT"
   }
   ```

2. **Payload (Carga útil)**: Contiene las "claims" (declaraciones) sobre el usuario
   ```json
   {
     "user_id": 1,
     "username": "admin",
     "exp": 1706740800
   }
   ```

3. **Signature (Firma)**: Verifica que el mensaje no ha sido alterado
   ```
   HMACSHA256(
     base64UrlEncode(header) + "." + base64UrlEncode(payload),
     SECRET_KEY
   )
   ```

### Implementación en el Proyecto

#### 1. Configuración (settings.py)

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

#### 2. Endpoints de Autenticación

**Login (Obtener Token)**
```
POST /api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "contraseña"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Refresh Token (Renovar Token)**
```
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Uso del Token

Para acceder a los endpoints protegidos, incluir el token en el header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Ventajas de JWT

1. **Stateless (Sin Estado)**: No necesita almacenar sesiones en el servidor
2. **Escalable**: Puede ser verificado en cualquier servidor que tenga la clave
3. **Seguro**: Firmado digitalmente para prevenir manipulación
4. **Eficiente**: Transmite información de forma compacta
5. **Cross-domain**: Funciona en diferentes dominios (ideal para APIs)

### Seguridad

- Los tokens tienen **expiración** (60 minutos para access, 1 día para refresh)
- La clave secreta se almacena en **variables de entorno**
- Todos los endpoints requieren **autenticación** (excepto login)
- Se usa **HTTPS** en producción para proteger la transmisión

## 3. Evidencias de Pruebas en Postman

### 3.1. Autenticación JWT

#### Login Exitoso (Admin)
```
POST http://localhost:8000/api/token/
Body:
{
    "username": "admin",
    "password": "admin123"
}

Status: 200 OK
Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Intento de Acceso Sin Token
```
GET http://localhost:8000/api/proyectos/

Status: 401 Unauthorized
Response:
{
    "detail": "Authentication credentials were not provided."
}
```

### 3.2. CRUD de Clientes (Solo Admin)

#### Crear Cliente
```
POST http://localhost:8000/api/clientes/
Headers:
  Authorization: Bearer <token_admin>
  Content-Type: application/json
Body:
{
    "nombre": "Juan Pérez",
    "email": "juan@empresa.com",
    "empresa": "Tech Solutions SPA"
}

Status: 201 Created
Response:
{
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@empresa.com",
    "empresa": "Tech Solutions SPA",
    "activo": true,
    "fecha_creacion": "2026-01-29T20:00:00Z",
    "proyectos": [],
    "total_proyectos": 0,
    "proyectos_activos": 0
}
```

#### Listar Clientes (Paginado)
```
GET http://localhost:8000/api/clientes/
Headers:
  Authorization: Bearer <token_admin>

Status: 200 OK
Response:
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@empresa.com",
            "empresa": "Tech Solutions SPA",
            "activo": true,
            "fecha_creacion": "2026-01-29T20:00:00Z",
            "total_proyectos": 2
        },
        ...
    ]
}
```

#### Eliminación Lógica
```
DELETE http://localhost:8000/api/clientes/1/
Headers:
  Authorization: Bearer <token_admin>

Status: 200 OK
Response:
{
    "detail": "Cliente desactivado exitosamente."
}
```

### 3.3. CRUD de Proyectos

#### Crear Proyecto (Admin)
```
POST http://localhost:8000/api/proyectos/
Headers:
  Authorization: Bearer <token_admin>
Body:
{
    "nombre": "Sistema ERP",
    "descripcion": "Desarrollo de sistema ERP para gestión empresarial",
    "estado": "En Desarrollo",
    "cliente": 1,
    "fecha_inicio": "2026-02-01",
    "fecha_entrega": "2026-08-31"
}

Status: 201 Created
Response:
{
    "id": 1,
    "nombre": "Sistema ERP",
    "descripcion": "Desarrollo de sistema ERP para gestión empresarial",
    "estado": "En Desarrollo",
    "progreso": 0,
    "cliente": 1,
    "cliente_nombre": "Juan Pérez",
    "cliente_empresa": "Tech Solutions SPA",
    "fecha_inicio": "2026-02-01",
    "fecha_entrega": "2026-08-31",
    "tareas": [],
    "total_tareas": 0,
    "tareas_completadas": 0
}
```

#### Filtrar Proyectos por Estado
```
GET http://localhost:8000/api/proyectos/?estado=En Desarrollo
Headers:
  Authorization: Bearer <token_admin>

Status: 200 OK
```

#### Cliente ve solo sus proyectos
```
GET http://localhost:8000/api/proyectos/
Headers:
  Authorization: Bearer <token_cliente>

Status: 200 OK
Response:
{
    "count": 2,
    "results": [
        // Solo proyectos donde cliente.email == usuario.email
    ]
}
```

### 3.4. CRUD de Tareas

#### Crear Tarea
```
POST http://localhost:8000/api/tareas/
Headers:
  Authorization: Bearer <token_admin>
Body:
{
    "titulo": "Diseño de Base de Datos",
    "descripcion": "Crear el modelo de datos del sistema",
    "estado": "En Progreso",
    "progreso": 75,
    "proyecto": 1
}

Status: 201 Created
```

#### Validación de Progreso Incorrecto
```
POST http://localhost:8000/api/tareas/
Body:
{
    "titulo": "Tarea Test",
    "progreso": 150,  // Error: fuera de rango
    "proyecto": 1
}

Status: 400 Bad Request
Response:
{
    "progreso": ["El progreso debe ser un número entero entre 0 y 100."]
}
```

### 3.5. Cálculo Automático de Progreso

#### Escenario
1. Proyecto creado con progreso inicial: 0%
2. Se crean 3 tareas con progresos: 50%, 75%, 100%
3. El progreso del proyecto se actualiza automáticamente

```
GET http://localhost:8000/api/proyectos/1/

Response:
{
    "id": 1,
    "nombre": "Sistema ERP",
    "progreso": 75,  // (50 + 75 + 100) / 3 = 75
    "total_tareas": 3,
    "tareas_completadas": 1
}
```

### 3.6. Permisos por Rol

#### Cliente intenta crear proyecto (Prohibido)
```
POST http://localhost:8000/api/proyectos/
Headers:
  Authorization: Bearer <token_cliente>

Status: 403 Forbidden
Response:
{
    "detail": "You do not have permission to perform this action."
}
```

#### Cliente accede a proyecto de otro cliente (Prohibido)
```
GET http://localhost:8000/api/proyectos/5/
Headers:
  Authorization: Bearer <token_cliente>

Status: 404 Not Found
// El proyecto existe pero no pertenece al cliente
```

### 3.7. SubTareas

#### Crear SubTarea
```
POST http://localhost:8000/api/subtareas/
Headers:
  Authorization: Bearer <token_admin>
Body:
{
    "titulo": "Diseñar diagrama ER",
    "completada": false,
    "tarea": 1
}

Status: 201 Created
```

#### Listar SubTareas Pendientes
```
GET http://localhost:8000/api/subtareas/pendientes/
Headers:
  Authorization: Bearer <token_admin>

Status: 200 OK
Response:
{
    "results": [
        // Solo subtareas con completada=false
    ]
}
```

## 4. Códigos HTTP y Respuestas

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 200 OK | Solicitud exitosa | GET exitoso |
| 201 Created | Recurso creado | POST exitoso |
| 400 Bad Request | Error de validación | Progreso > 100 |
| 401 Unauthorized | No autenticado | Sin token |
| 403 Forbidden | Sin permisos | Cliente intenta DELETE |
| 404 Not Found | Recurso no existe | GET /proyectos/999/ |

## 5. Validaciones Implementadas

1. **Progreso**: Debe estar entre 0 y 100
2. **Email**: Único para cada cliente
3. **Fechas**: fecha_entrega > fecha_inicio
4. **Estados**: Solo valores permitidos
5. **SubTarea**: Solo se completa si tiene tarea asociada
6. **Aislamiento**: Cliente solo accede a sus datos

## 6. Filtros Disponibles

### Proyectos
- `?estado=En Desarrollo`
- `?cliente=1`
- `?search=nombre_proyecto`
- `?ordering=-fecha_inicio`

### Tareas
- `?proyecto=1`
- `?estado=Completada`
- `?search=titulo_tarea`

### SubTareas
- `?tarea=1`
- `?completada=true`

## 7. Paginación

Todos los listados incluyen:
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/proyectos/?page=3",
    "previous": "http://localhost:8000/api/proyectos/?page=1",
    "results": [...]
}
```

## 8. Cumplimiento de Requerimientos

### Configuración Inicial (3.1.1) ✅
- [x] Proyecto Django creado
- [x] Django Rest Framework configurado
- [x] Conexión a MySQL configurada
- [x] Aplicación `core` creada

### Autenticación y Seguridad (3.1.2) ✅
- [x] JWT implementado (login + refresh)
- [x] Todos los endpoints protegidos
- [x] IsAuthenticated obligatorio
- [x] SECRET_KEY en variables de entorno

### Roles ✅
- [x] Administrador: CRUD completo
- [x] Cliente: Solo lectura de sus datos
- [x] Aislamiento de datos por cliente

### Modelos de Datos ✅
- [x] Cliente con todos los campos
- [x] Proyecto con relación a Cliente
- [x] Tarea con relación a Proyecto
- [x] SubTarea con relación a Tarea

### Endpoints RESTful ✅
- [x] CRUD completo para todos los modelos
- [x] Eliminación lógica en Clientes
- [x] Respuestas en formato JSON
- [x] Códigos HTTP correctos

### Reglas Avanzadas ✅
- [x] Paginación implementada
- [x] Filtros por cliente, estado, proyecto
- [x] Validación de progreso (0-100)
- [x] Cálculo automático de progreso
- [x] Validación de SubTarea
- [x] Respuestas HTTP correctas

## 9. Notas de Seguridad

- ✅ Nunca exponer SECRET_KEY en el código
- ✅ Usar HTTPS en producción
- ✅ Los tokens expiran automáticamente
- ✅ Validación de permisos en cada request
- ✅ Aislamiento de datos por usuario
