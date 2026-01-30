from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, Proyecto, Tarea, SubTarea
from .serializers import (
    RegisterSerializer,
    ClienteSerializer,
    ProyectoSerializer,
    TareaSerializer,
    SubTareaSerializer
)
from .permissions import IsOwnerOrAdmin


class RegisterView(APIView):
    """Vista para registrar nuevos usuarios."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Usuario creado exitosamente"},
            status=status.HTTP_201_CREATED
        )


class ClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Clientes (Solo Administradores)."""
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['activo', 'empresa']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        # Admin ve todos los clientes
        if profile and profile.role == 'ADMIN':
            return Cliente.objects.all()
        
        # Los clientes no pueden listar otros clientes
        return Cliente.objects.none()

    def perform_destroy(self, instance):
        """Eliminación lógica: marca como inactivo."""
        instance.activo = False
        instance.save()

    def destroy(self, request, *args, **kwargs):
        """Sobrescribe destroy para retornar respuesta apropiada."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Cliente desactivado exitosamente."},
            status=status.HTTP_200_OK
        )


class ProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Proyectos."""
    serializer_class = ProyectoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'cliente']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        # Admin ve todos los proyectos
        if profile and profile.role == 'ADMIN':
            return Proyecto.objects.all()
        
        # Los clientes solo ven sus proyectos
        # Asumiendo que existe una relación entre Cliente y User
        return Proyecto.objects.none()

    def perform_create(self, serializer):
        """Crea el proyecto y actualiza progreso."""
        proyecto = serializer.save()
        proyecto.actualizar_progreso()


class TareaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Tareas."""
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'proyecto']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        # Admin ve todas las tareas
        if profile and profile.role == 'ADMIN':
            return Tarea.objects.all()
        
        # Los clientes solo ven tareas de sus proyectos
        return Tarea.objects.none()

    def perform_create(self, serializer):
        """Crea la tarea y actualiza progreso del proyecto."""
        tarea = serializer.save()
        tarea.proyecto.actualizar_progreso()

    def perform_update(self, serializer):
        """Actualiza la tarea y recalcula progreso del proyecto."""
        tarea = serializer.save()
        tarea.proyecto.actualizar_progreso()


class SubTareaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar SubTareas."""
    serializer_class = SubTareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tarea', 'completada']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        # Admin ve todas las subtareas
        if profile and profile.role == 'ADMIN':
            return SubTarea.objects.all()
        
        # Los clientes solo ven subtareas de sus tareas
        return SubTarea.objects.none()

