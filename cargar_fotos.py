# -*- coding: utf-8 -*-
import os
import sys
import django
from django.core.files import File

# Redirigir salida a UTF-8 para evitar error de encoding en Windows
sys.stdout.reconfigure(encoding='utf-8')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile


def subir_imagenes():
    # DICCIONARIO: nombre de usuario Django -> nombre del archivo en media/profile_pics
    USUARIOS_FOTOS = {
        'marcelo':  'marcelo_profile.jpg',   # Marcelo
        'aridna':   'ariadna_profile.png',   # Ariadna
        'lonapoli': 'lonapoli.jpg',          # Luis Lonapoli
        'nnapoli':  'nnapoli.jpg',           # Nicolas
        'Farias':   'farias.jpg',            # Federico Farias
        'anorak':   'anorak.jpg',            # Matias
    }

    base_dir = 'media/profile_pics'

    print("--- INICIANDO CARGA A CLOUDINARY ---")

    for username, filename in USUARIOS_FOTOS.items():
        try:
            user = User.objects.filter(username__iexact=username).first()

            if not user:
                print(f"  [ERROR] Usuario '{username}' no encontrado en la base de datos.")
                continue

            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                print(f"  [INFO] Perfil de {username} creado.")

            file_path = os.path.join(base_dir, filename)

            if os.path.exists(file_path):
                print(f"  Subiendo '{filename}' para {username}...")
                with open(file_path, 'rb') as f:
                    profile.image.save(filename, File(f), save=True)
                print(f"  [OK] {username} -> foto subida correctamente a Cloudinary.")
            else:
                print(f"  [WARN] Archivo no encontrado: {file_path}")

        except Exception as e:
            print(f"  [ERROR] {username}: {str(e)}")

    print("--- FIN ---")


if __name__ == '__main__':
    subir_imagenes()