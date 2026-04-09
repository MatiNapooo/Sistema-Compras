# -*- coding: utf-8 -*-
"""
Actualiza los perfiles en la base de datos de Heroku con las rutas de Cloudinary.
Se corre en Heroku via: heroku run python actualizar_db_fotos.py --app compras-nextprint
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

# Mapeo: username exacto -> public_id en Cloudinary (carpeta/nombre)
# Formato que usa django-cloudinary-storage para el campo ImageField
USUARIOS_CLOUDINARY = {
    'marcelo':  'profile_pics/marcelo',
    'aridna':   'profile_pics/aridna',
    'lonapoli': 'profile_pics/lonapoli',
    'nnapoli':  'profile_pics/nnapoli',
    'Farias':   'profile_pics/Farias',
    'anorak':   'profile_pics/anorak',
}

print("--- ACTUALIZANDO DB CON RUTAS DE CLOUDINARY ---")

for username, cloudinary_path in USUARIOS_CLOUDINARY.items():
    try:
        user = User.objects.filter(username=username).first()
        if not user:
            print(f"  [ERROR] Usuario '{username}' no encontrado.")
            continue

        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            print(f"  [INFO] Perfil de '{username}' creado.")

        profile.image = cloudinary_path
        profile.save()
        print(f"  [OK] {username} -> {cloudinary_path}")

    except Exception as e:
        print(f"  [ERROR] {username}: {e}")

print()
print("--- FIN. Los perfiles ahora apuntan a Cloudinary. ---")
