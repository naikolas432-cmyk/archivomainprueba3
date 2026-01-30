from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Cliente, Proyecto, Tarea, SubTarea


class ProfileInline(admin.StackedInline):
    """Inline para editar Profile desde el User."""
    model = Profile
    fields = ['role']


class CustomUserAdmin(BaseUserAdmin):
    """Extensión del admin de Usuario con Profile."""
    inlines = [ProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'empresa', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'empresa', 'fecha_creacion']
    search_fields = ['nombre', 'email', 'empresa']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'estado', 'progreso', 'fecha_inicio', 'fecha_entrega']
    list_filter = ['estado', 'cliente', 'fecha_inicio']
    search_fields = ['nombre', 'descripcion']
    ordering = ['-fecha_inicio']
    readonly_fields = ['progreso']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'cliente')
        }),
        ('Estado y Progreso', {
            'fields': ('estado', 'progreso')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_entrega')
        }),
    )


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'estado', 'progreso', 'fecha_creacion']
    list_filter = ['estado', 'proyecto', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']


@admin.register(SubTarea)
class SubTareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tarea', 'completada', 'fecha_creacion']
    list_filter = ['completada', 'tarea', 'fecha_creacion']
    search_fields = ['titulo']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']
