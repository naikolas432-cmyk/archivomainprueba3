# Script de Comandos Útiles - API Gestión de Proyectos

## Instalación y Configuración

### 1. Crear y activar entorno virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```powershell
# Copiar el archivo de ejemplo
Copy-Item .env.example .env
# Editar .env con tus credenciales
notepad .env
```

### 4. Crear base de datos MySQL
```sql
-- Ejecutar en MySQL Workbench o cliente MySQL
CREATE DATABASE gestor_proyectos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Ejecutar migraciones
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario (Administrador)
```powershell
python manage.py createsuperuser
```

### 7. Iniciar servidor de desarrollo
```powershell
python manage.py runserver
```

## Comandos de Desarrollo

### Crear nuevas migraciones
```powershell
python manage.py makemigrations core
```

### Aplicar migraciones
```powershell
python manage.py migrate
```

### Ver migraciones aplicadas
```powershell
python manage.py showmigrations
```

### Crear superusuario
```powershell
python manage.py createsuperuser
```

### Acceder al shell de Django
```powershell
python manage.py shell
```

### Verificar configuración
```powershell
python manage.py check
```

### Limpiar base de datos y recrear
```powershell
# ⚠️ CUIDADO: Elimina todos los datos
python manage.py flush
```

## Comandos de Base de Datos

### Crear base de datos en MySQL
```sql
CREATE DATABASE gestor_proyectos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Ver SQL de migraciones sin aplicar
```powershell
python manage.py sqlmigrate core 0001
```

### Hacer backup de la base de datos
```powershell
# Desde línea de comandos (MySQL)
mysqldump -u root -p gestor_proyectos > backup.sql
```

### Restaurar backup
```powershell
mysql -u root -p gestor_proyectos < backup.sql
```

## Pruebas y Depuración

### Ejecutar pruebas
```powershell
python manage.py test
```

### Ejecutar pruebas con detalle
```powershell
python manage.py test --verbosity=2
```

### Ver configuración actual
```powershell
python manage.py diffsettings
```

## Gestión de Usuarios (En Shell)

### Crear usuario administrador programáticamente
```python
python manage.py shell

from django.contrib.auth.models import User
admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
admin.save()
```

### Crear usuario cliente programáticamente
```python
from django.contrib.auth.models import User
cliente = User.objects.create_user('cliente1', 'cliente1@example.com', 'cliente123')
cliente.is_staff = False
cliente.save()
```

### Listar todos los usuarios
```python
from django.contrib.auth.models import User
User.objects.all()
```

## Datos de Prueba

### Crear datos de prueba en Shell
```python
python manage.py shell

# Importar modelos
from core.models import Cliente, Proyecto, Tarea, SubTarea
from datetime import date, timedelta

# Crear cliente
cliente = Cliente.objects.create(
    nombre="Juan Pérez",
    email="juan@empresa.com",
    empresa="Tech Solutions SPA"
)

# Crear proyecto
proyecto = Proyecto.objects.create(
    nombre="Sistema ERP",
    descripcion="Desarrollo de sistema de gestión empresarial",
    estado="En Desarrollo",
    cliente=cliente,
    fecha_inicio=date.today(),
    fecha_entrega=date.today() + timedelta(days=180)
)

# Crear tarea
tarea = Tarea.objects.create(
    titulo="Diseño de Base de Datos",
    descripcion="Crear el modelo de datos del sistema",
    estado="En Progreso",
    progreso=75,
    proyecto=proyecto
)

# Crear subtarea
subtarea = SubTarea.objects.create(
    titulo="Diseñar diagrama ER",
    completada=False,
    tarea=tarea
)

# Verificar
print(f"Proyecto: {proyecto.nombre}, Progreso: {proyecto.progreso}%")
```

## Endpoints de la API

### Autenticación
```bash
# Obtener token (Login)
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Refrescar token
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<token_refresh>"}'
```

### Clientes (Admin)
```bash
# Listar clientes
curl http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <token>"

# Crear cliente
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","email":"juan@empresa.com","empresa":"Tech Solutions"}'

# Ver detalle
curl http://localhost:8000/api/clientes/1/ \
  -H "Authorization: Bearer <token>"

# Actualizar
curl -X PUT http://localhost:8000/api/clientes/1/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","email":"juan@empresa.com","empresa":"Tech Solutions SPA"}'

# Eliminar (lógico)
curl -X DELETE http://localhost:8000/api/clientes/1/ \
  -H "Authorization: Bearer <token>"
```

### Proyectos
```bash
# Listar proyectos
curl http://localhost:8000/api/proyectos/ \
  -H "Authorization: Bearer <token>"

# Filtrar por estado
curl "http://localhost:8000/api/proyectos/?estado=En Desarrollo" \
  -H "Authorization: Bearer <token>"

# Crear proyecto
curl -X POST http://localhost:8000/api/proyectos/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Sistema ERP","descripcion":"Desarrollo ERP","estado":"En Desarrollo","cliente":1,"fecha_inicio":"2026-02-01","fecha_entrega":"2026-08-31"}'
```

### Tareas
```bash
# Listar tareas
curl http://localhost:8000/api/tareas/ \
  -H "Authorization: Bearer <token>"

# Filtrar por proyecto
curl "http://localhost:8000/api/tareas/?proyecto=1" \
  -H "Authorization: Bearer <token>"

# Crear tarea
curl -X POST http://localhost:8000/api/tareas/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Diseño de BD","descripcion":"Crear modelo de datos","estado":"En Progreso","progreso":75,"proyecto":1}'
```

### SubTareas
```bash
# Listar subtareas
curl http://localhost:8000/api/subtareas/ \
  -H "Authorization: Bearer <token>"

# Listar pendientes
curl http://localhost:8000/api/subtareas/pendientes/ \
  -H "Authorization: Bearer <token>"

# Crear subtarea
curl -X POST http://localhost:8000/api/subtareas/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Diseñar diagrama ER","completada":false,"tarea":1}'
```

## URLs Importantes

- **API Base**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Login**: http://localhost:8000/api/token/
- **API Refresh**: http://localhost:8000/api/token/refresh/
- **Clientes**: http://localhost:8000/api/clientes/
- **Proyectos**: http://localhost:8000/api/proyectos/
- **Tareas**: http://localhost:8000/api/tareas/
- **SubTareas**: http://localhost:8000/api/subtareas/

## Solución de Problemas

### Error: No module named 'core'
```powershell
# Asegurarse de que core esté en INSTALLED_APPS
python manage.py check
```

### Error: Access denied for user
```powershell
# Verificar credenciales en .env
# Verificar que MySQL esté corriendo
# Verificar que la base de datos exista
```

### Error: Migrations not applied
```powershell
python manage.py migrate
```

### Error: SECRET_KEY not set
```powershell
# Crear archivo .env con SECRET_KEY
# O establecer variable de entorno
```

### Puerto 8000 en uso
```powershell
# Usar otro puerto
python manage.py runserver 8080
```

## Mejores Prácticas

1. **Siempre usar entorno virtual**
2. **Nunca commitear .env**
3. **Mantener requirements.txt actualizado**
4. **Hacer migraciones después de cambiar modelos**
5. **Usar tokens JWT con expiración**
6. **Validar permisos en cada endpoint**
7. **Documentar cambios importantes**
8. **Hacer backup de la base de datos regularmente**

## Variables de Entorno Requeridas

```
SECRET_KEY=<tu-clave-secreta>
DB_NAME=gestor_proyectos
DB_USER=root
DB_PASSWORD=<tu-password>
DB_HOST=127.0.0.1
DB_PORT=3306
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```
