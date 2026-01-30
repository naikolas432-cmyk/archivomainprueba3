from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # [cite: 51] Acceso al panel de administración
    path('admin/', admin.site.urls), 
    
    #  Endpoints para autenticación JWT (Login y Refresh)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # [cite: 62] Inclusión de las rutas de la aplicación core
    path('api/', include('core.urls')),
]