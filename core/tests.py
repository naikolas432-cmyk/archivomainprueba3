from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Profile, Cliente, Proyecto, Tarea, SubTarea


class RegisterTests(APITestCase):
    """Tests para el endpoint de registro de usuarios."""
    
    def test_register_creates_user_and_profile_role(self):
        """Verifica que el registro cree usuario y asigne rol."""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'strongpass123',
            'email': 'test@example.com',
            'role': 'CLIENT'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(username='newuser')
        self.assertEqual(user.profile.role, 'CLIENT')


class ProjectTaskTests(APITestCase):
    """Tests para proyectos, tareas y filtrado."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        # Crear usuarios
        self.admin = User.objects.create_user('admin', password='adminpass')
        self.admin.profile.role = 'ADMIN'
        self.admin.profile.save()

        self.user = User.objects.create_user('user1', password='userpass')
        self.user.profile.role = 'CLIENT'
        self.user.profile.save()

        # Crear clientes
        self.client_obj = Cliente.objects.create(
            nombre='Cliente 1',
            email='cliente1@example.com',
            empresa='Empresa 1'
        )

        # Crear proyectos
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto 1',
            descripcion='Descripción del proyecto',
            cliente=self.client_obj,
            fecha_inicio='2025-01-01',
            fecha_entrega='2025-12-31'
        )

        # Crear tarea
        self.tarea = Tarea.objects.create(
            titulo='Tarea 1',
            descripcion='Descripción de tarea',
            proyecto=self.proyecto,
            progreso=0
        )

    def test_clientes_list_admin_sees_all(self):
        """Admin puede ver todos los clientes."""
        url = reverse('clientes-list')
        
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_proyectos_list_filtering(self):
        """Los proyectos pueden filtrarse por cliente."""
        url = reverse('proyectos-list')
        
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get(url + f'?cliente={self.client_obj.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_tarea_creation_updates_proyecto_progreso(self):
        """Crear una tarea debe actualizar progreso del proyecto."""
        url = reverse('tareas-list')
        
        self.client.force_authenticate(user=self.admin)
        data = {
            'titulo': 'Nueva Tarea',
            'descripcion': 'Descripción',
            'proyecto': self.proyecto.id,
            'progreso': 50
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el progreso se actualiza
        self.proyecto.refresh_from_db()
        self.assertGreater(self.proyecto.progreso, 0)


class CRUDPermissionsTests(APITestCase):
    """Tests para permisos y control de acceso."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.admin = User.objects.create_user('admin2', password='adminpass')
        self.admin.profile.role = 'ADMIN'
        self.admin.profile.save()

        self.user = User.objects.create_user('userA', password='userpass')
        self.user.profile.role = 'CLIENT'
        self.user.profile.save()

        self.other = User.objects.create_user('userB', password='otherpass')
        self.other.profile.role = 'CLIENT'
        self.other.profile.save()

        # Crear cliente
        self.cliente_obj = Cliente.objects.create(
            nombre='Test Cliente',
            email='test@example.com',
            empresa='Test Corp'
        )

        # Crear proyecto
        self.proyecto = Proyecto.objects.create(
            nombre='Test Proyecto',
            descripcion='Test',
            cliente=self.cliente_obj,
            fecha_inicio='2025-01-01',
            fecha_entrega='2025-12-31'
        )

    def _patch(self, url, data, user):
        """Helper para hacer PATCH."""
        self.client.force_authenticate(user=user)
        return self.client.patch(url, data, format='json')

    def _put(self, url, data, user):
        """Helper para hacer PUT."""
        self.client.force_authenticate(user=user)
        return self.client.put(url, data, format='json')

    def _delete(self, url, user):
        """Helper para hacer DELETE."""
        self.client.force_authenticate(user=user)
        return self.client.delete(url)

    def test_proyecto_patch_put_delete_admin_only(self):
        """Solo admin puede PATCH/PUT/DELETE proyectos."""
        url = reverse('proyectos-detail', args=[self.proyecto.id])

        # Admin puede patch
        resp = self._patch(url, {'nombre': 'P1-nuevo'}, self.admin)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Client no puede patch (404 - objeto no visible)
        resp = self._patch(url, {'nombre': 'bad'}, self.user)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # Admin puede delete
        resp = self._delete(url, self.admin)
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))

    def test_tarea_crud_permissions(self):
        """Tests de permisos CRUD para tareas."""
        tarea = Tarea.objects.create(
            titulo='Test Task',
            descripcion='Test',
            proyecto=self.proyecto,
            progreso=0
        )
        
        url = reverse('tareas-detail', args=[tarea.id])

        # Admin puede actualizar
        resp = self._patch(url, {'titulo': 'Task Actualizada'}, self.admin)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Client no puede ver (404)
        resp = self._patch(url, {'titulo': 'x'}, self.user)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
