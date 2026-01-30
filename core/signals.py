from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un Profile cuando se crea un nuevo Usuario."""
    if created:
        Profile.objects.create(user=instance, role='CLIENT')


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Guarda el Profile cuando se guarda el Usuario."""
    instance.profile.save()
