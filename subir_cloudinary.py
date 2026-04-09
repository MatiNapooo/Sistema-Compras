# -*- coding: utf-8 -*-
"""
Script para subir fotos directamente a Cloudinary usando el SDK.
Luego actualiza la base de datos de Heroku con la URL de cada foto.
Corre este script localmente con el venv activado.
"""
import cloudinary
import cloudinary.uploader
import os
import sys

# Configurar Cloudinary directamente
cloudinary.config(
    cloud_name="dvinasjl9",
    api_key="331969733158713",
    api_secret="4-ACWlJhFEq351-TYPbi9IRYoeM"
)

# Mapeo: username -> archivo local
USUARIOS_FOTOS = {
    'marcelo':  'media/profile_pics/marcelo_profile.jpg',
    'aridna':   'media/profile_pics/ariadna_profile.png',
    'lonapoli': 'media/profile_pics/lonapoli.jpg',
    'nnapoli':  'media/profile_pics/nnapoli.jpg',
    'Farias':   'media/profile_pics/farias.jpg',
    'anorak':   'media/profile_pics/anorak.jpg',
}

print("--- SUBIENDO FOTOS A CLOUDINARY ---")
print()

resultados = {}

for username, filepath in USUARIOS_FOTOS.items():
    if not os.path.exists(filepath):
        print(f"  [WARN] No se encontro: {filepath}")
        continue

    try:
        print(f"  Subiendo {filepath}...")
        result = cloudinary.uploader.upload(
            filepath,
            folder="profile_pics",
            public_id=username,
            overwrite=True,
            resource_type="image"
        )
        url = result.get("secure_url", "")
        resultados[username] = url
        print(f"  [OK] {username} -> {url}")
    except Exception as e:
        print(f"  [ERROR] {username}: {e}")

print()
print("--- RESULTADOS FINALES ---")
for user, url in resultados.items():
    print(f"  {user}: {url}")

print()
print("Ahora hay que actualizar la base de datos de Heroku.")
print("Correr: heroku run python actualizar_db_fotos.py --app compras-nextprint")
