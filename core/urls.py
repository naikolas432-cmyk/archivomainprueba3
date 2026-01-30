from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    ClienteViewSet,
    ProyectoViewSet,
    TareaViewSet,
    SubTareaViewSet
)

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
