# -*- coding: utf-8 -*-
"""
Actualiza la DB de Heroku directamente via SQL.
Los perfiles existentes pueden tener nombres con sufijos (e.g. nnapoli_ssmxDU2.jpg).
Este script los sobreescribe con el path correcto de Cloudinary.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

USUARIOS_CLOUDINARY = {
    'Marcelo':   'profile_pics/marcelo',
    'Ariadna':   'profile_pics/aridna',
    'Lonapoli':  'profile_pics/lonapoli',
    'Nicolas':   'profile_pics/nnapoli',
    'Federico':  'profile_pics/Farias',
    'anorak':    'profile_pics/anorak',
}

print("--- ACTUALIZANDO DB CON CLOUDINARY PATHS ---")

for username, cloudinary_path in USUARIOS_CLOUDINARY.items():
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"SKIP: usuario '{username}' no existe")
        continue
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        print(f"INFO: Perfil creado para '{username}'")
    profile.image = cloudinary_path
    profile.save()
    print(f"OK: {username} -> {cloudinary_path}")

print("--- FIN ---")
