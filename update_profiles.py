import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

# Map usernames to filenames
images = {
    'nnapoli': 'profile_pics/nnapoli.jpg',
    'lonapoli': 'profile_pics/lonapoli.jpg',
}

for username, image_path in images.items():
    try:
        user = User.objects.get(username=username)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.image = image_path
        profile.save()
        print(f"Imagen actualizada para {username}")
    except User.DoesNotExist:
        print(f"Usuario {username} no encontrado")
    except Exception as e:
        print(f"Error actualizando {username}: {e}")

print("Proceso de imagenes finalizado.")
