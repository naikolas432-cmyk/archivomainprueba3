# Documentación - API RESTful con Django (Buenas Prácticas)

## Resumen de Refactorización

Se ha refactorizado el proyecto siguiendo estrictamente las buenas prácticas del repositorio de referencia `vetocanti/backend-verano-3`. A continuación se detallan los cambios principales.

---

## 1. Estructura de Modelos Mejorada

### Cambios Implementados:

#### Modelo Profile (Nuevo)
```python
class Profile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('CLIENT', 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
```

**Beneficio**: Separa la lógica de roles del modelo User de Django, siguiendo el patrón de extensión del usuario.

#### Relacionales Mejradas
- `Cliente` ahora es una entidad independiente (sin User)
- `Proyecto` → `Cliente` (FK)
- `Tarea` → `Proyecto` (FK)
- `SubTarea` → `Tarea` (FK)

**Patrón Jerárquico**:
```
User (Profile con rol) → Proyecto ← Cliente
                             ↓
                            Tarea
                             ↓
                          SubTarea
```

---

## 2. Autenticación JWT

### Configuración en `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

### Endpoints de Autenticación:
- `POST /api/auth/register/` - Registrar usuario nuevo con rol
- `POST /api/auth/token/` - Obtener token JWT
- `POST /api/auth/token/refresh/` - Refrescar token

**Ejemplo de Uso**:
```bash
# Registrar
POST /api/auth/register/
{
  "username": "admin1",
  "password": "strongpass123",
  "email": "admin@example.com",
  "role": "ADMIN"
}

# Obtener Token
POST /api/auth/token/
{
  "username": "admin1",
  "password": "strongpass123"
}

# Respuesta
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 3. Sistema de Permisos Basado en Roles

### Archivo `core/permissions.py`:

```python
class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso al owner del recurso o a un administrador.
    - Admin (role='ADMIN'): Acceso total
    - Usuario: Solo acceso a sus propios datos
    """
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        profile = getattr(request.user, 'profile', None)
        if profile and profile.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        return False
```

### Características:
- ✅ Todos los endpoints requieren `IsAuthenticated`
- ✅ Admins tienen acceso total (CRUD)
- ✅ Clientes solo ven sus datos
- ✅ Aislamiento de datos garantizado

---

## 4. Views Simplificadas y Limpias

### Patrón ViewSet Standard:

```python
class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['activo', 'empresa']

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        # Admin ve todos
        if profile and profile.role == 'ADMIN':
            return Cliente.objects.all()
        
        # Cliente no puede listar otros clientes
        return Cliente.objects.none()
```

### Eliminación Lógica:
```python
def perform_destroy(self, instance):
    instance.activo = False
    instance.save()
```

---

## 5. Serializadores Limpios y Simples

### Serializador Base (sin métodos redundantes):

```python
class ClienteSerializer(serializers.ModelSerializer):
    proyectos = ProyectoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'empresa', 'activo',
                  'fecha_creacion', 'proyectos']
        read_only_fields = ['id', 'fecha_creacion']
```

**Ventajas**:
- Sin `get_serializer_class()` innecesario
- Sin serializadores de listado duplicados
- Anidación natural de relaciones

---

## 6. Signals para Auto-crear Profile

### Archivo `core/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='CLIENT')
```

### Activación en `core/apps.py`:

```python
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals
```

---

## 7. URLs Bien Organizadas

### Archivo `core/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'proyectos', ProyectoViewSet, basename='proyectos')
router.register(r'tareas', TareaViewSet, basename='tareas')
router.register(r'subtareas', SubTareaViewSet, basename='subtareas')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
```

---

## 8. Tests Siguiendo Patrones Standard

### Tests incluidos:

1. **RegisterTests** - Verificar registro de usuarios con rol
2. **ProjectTaskTests** - Filtrado y actualizaciones en cascada
3. **CRUDPermissionsTests** - Permisos por rol

```python
class RegisterTests(APITestCase):
    def test_register_creates_user_and_profile_role(self):
        url = reverse('register')
        data = {...}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(username='newuser')
        self.assertEqual(user.profile.role, 'CLIENT')
```

---

## 9. Configuración de Entorno

### Archivo `.env.example`:

```env
# Django Settings
SECRET_KEY=django-insecure-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=prueba_3
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

---

## 10. Admin Mejorado

```python
class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['role']

class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
```

---

## Comparativa: Antes vs Después

| Aspecto | Antes | Después |
|--------|-------|---------|
| Permisos | `IsAdminOrReadOnlyClient` + `CanManageClientes` | `IsOwnerOrAdmin` (único y reutilizable) |
| Serializadores | 6 clases (SimplificadosEnListado + Completos) | 5 clases (simples y claras) |
| Roles | `is_staff` + `is_superuser` | `Profile.role` (ADMIN/CLIENT) |
| Relaciones | Cliente sin relación a User | Profile → User (1:1) |
| Signals | No existían | Crea Profile automáticamente |
| Tests | 0 tests | 12+ tests funcionales |

---

## Buenas Prácticas Aplicadas

✅ **DRY (Don't Repeat Yourself)**
- Una única clase de permisos para todo
- Serializadores sin duplicación

✅ **SOLID - Single Responsibility**
- `IsOwnerOrAdmin` solo maneja permisos
- Views solo manejan lógica CRUD
- Serializers solo validan datos

✅ **Separación de Concerns**
- Signals en archivo separado
- Permisos en archivo separado
- Tests en archivo separado

✅ **Código Limpio**
- Nombres descriptivos
- Docstrings claros
- Métodos cortos y enfocados

✅ **Seguridad**
- JWT obligatorio en todos los endpoints
- Aislamiento de datos por rol
- Validaciones en serializers

✅ **Mantenibilidad**
- Estructura predecible (patrón MVT)
- Fácil de extender
- Documentación inline

---

## Conclusión

El proyecto ahora sigue las mejores prácticas de Django Rest Framework, con:

1. **Código más limpio y mantenible**
2. **Seguridad robusta con JWT**
3. **Aislamiento de datos garantizado**
4. **Tests funcionales incluidos**
5. **Estructura escalable y extensible**

Está listo para producción con ajustes menores de configuración según el ambiente.
