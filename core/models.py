from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Modelo Profile: Extensión de Usuario con roles
class Profile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('CLIENT', 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Modelo Cliente: Almacena la información de la empresa contratante.
class Cliente(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Cliente")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Garantiza que no existan correos duplicados.")
    empresa = models.CharField(max_length=255, verbose_name="Empresa")
    activo = models.BooleanField(default=True, verbose_name="Activo", help_text="Para implementar la eliminación lógica.")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} ({self.empresa})"

# Modelo Proyecto: Representa el esfuerzo principal asociado a un cliente.
class Proyecto(models.Model):
    ESTADOS_PROYECTO = [
        ('Pendiente', 'Pendiente'),
        ('En Desarrollo', 'En Desarrollo'),
        ('En Pruebas', 'En Pruebas'),
        ('Finalizado', 'Finalizado'),
    ]
    
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_PROYECTO, 
        default='Pendiente',
        verbose_name="Estado"
    )
    progreso = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Progreso (%)",
        help_text="Progreso del proyecto entre 0 y 100"
    )
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='proyectos',
        verbose_name="Cliente"
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_entrega = models.DateField(verbose_name="Fecha de Entrega")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_inicio']

    def actualizar_progreso(self):
        """Lógica avanzada: Cálculo automático del progreso basado en tareas."""
        tareas = self.tareas.all()
        if tareas.exists():
            total_progreso = sum(t.progreso for t in tareas)
            self.progreso = int(total_progreso / tareas.count())
            self.save(update_fields=['progreso'])

    def clean(self):
        """Validación personalizada: fecha_entrega debe ser mayor a fecha_inicio."""
        if self.fecha_entrega and self.fecha_inicio and self.fecha_entrega < self.fecha_inicio:
            raise ValidationError("La fecha de entrega debe ser posterior a la fecha de inicio.")

    def __str__(self):
        return self.nombre

# Modelo Tarea: Desglose de actividades de un proyecto.
class Tarea(models.Model):
    ESTADOS_TAREA = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Bloqueada', 'Bloqueada'),
        ('Completada', 'Completada'),
    ]
    
    titulo = models.CharField(max_length=255, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_TAREA, 
        default='Pendiente',
        verbose_name="Estado"
    )
    progreso = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Progreso (%)",
        help_text="Progreso de la tarea entre 0 y 100"
    )
    proyecto = models.ForeignKey(
        Proyecto, 
        on_delete=models.CASCADE, 
        related_name='tareas',
        verbose_name="Proyecto"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['-fecha_creacion']

    def save(self, *args, **kwargs):
        """Sobrecarga del método save para disparar el recálculo en el Proyecto padre."""
        super().save(*args, **kwargs)
        self.proyecto.actualizar_progreso()

    def __str__(self):
        return f"{self.titulo} - {self.proyecto.nombre}"

# Modelo SubTarea: Nivel mínimo de detalle de una tarea.
class SubTarea(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    completada = models.BooleanField(default=False, verbose_name="Completada")
    tarea = models.ForeignKey(
        Tarea, 
        on_delete=models.CASCADE, 
        related_name='subtareas',
        verbose_name="Tarea"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "SubTarea"
        verbose_name_plural = "SubTareas"
        ordering = ['-fecha_creacion']

    def clean(self):
        """Validación: Una SubTarea solo puede marcarse como completada si pertenece a una tarea existente."""
        if self.completada and not self.tarea_id:
            raise ValidationError("Una subtarea debe estar asociada a una tarea para ser marcada como completada.")

    def __str__(self):
        return self.titulo
