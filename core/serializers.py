from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Cliente, Proyecto, Tarea, SubTarea


class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para registrar nuevos usuarios con rol."""
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=['ADMIN', 'CLIENT'], default='CLIENT')

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        """Crea el usuario y asigna el rol en el Profile."""
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        user.profile.role = role
        user.profile.save()
        return user


class SubTareaSerializer(serializers.ModelSerializer):
    """Serializador para SubTareas."""
    
    class Meta:
        model = SubTarea
        fields = ['id', 'titulo', 'completada', 'tarea', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class TareaSerializer(serializers.ModelSerializer):
    """Serializador para Tareas con SubTareas anidadas."""
    subtareas = SubTareaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'estado', 'progreso', 
                  'proyecto', 'fecha_creacion', 'subtareas']
        read_only_fields = ['id', 'fecha_creacion']


class ProyectoSerializer(serializers.ModelSerializer):
    """Serializador para Proyectos con Tareas anidadas."""
    tareas = TareaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'estado', 'progreso',
                  'cliente', 'fecha_inicio', 'fecha_entrega', 'tareas']
        read_only_fields = ['id', 'progreso']


class ClienteSerializer(serializers.ModelSerializer):
    """Serializador para Clientes con Proyectos anidados."""
    proyectos = ProyectoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'empresa', 'activo',
                  'fecha_creacion', 'proyectos']
        read_only_fields = ['id', 'fecha_creacion']
