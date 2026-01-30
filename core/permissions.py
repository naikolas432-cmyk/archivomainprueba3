from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso al owner del recurso o a un administrador.
    - Admin (role='ADMIN'): Acceso total
    - Usuario: Solo acceso a sus propios datos
    """
    
    def has_permission(self, request, view):
        """Requiere autenticación para todas las acciones."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Verifica si el usuario es owner o admin."""
        # Admin puede acceder a todo
        profile = getattr(request.user, 'profile', None)
        if profile and profile.role == 'ADMIN':
            return True
        
        # Usuario solo accede a sus datos
        # Para Cliente: comparar el usuario autenticado
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Para otros modelos: owner es el usuario
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # Para Proyecto con cliente: cliente debe tener usuario asociado
        if hasattr(obj, 'cliente'):
            # El cliente debe ser el usuario autenticado si es CLIENT
            return obj.cliente.user == request.user if hasattr(obj.cliente, 'user') else False
        
        return False

