import os
import django
from django.core.files import File

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile  # <--- IMPORTANTE: Traemos el modelo Profile

def subir_imagenes():
    # --- DICCIONARIO: USUARIO vs ARCHIVO ---
    # Asegúrate que los nombres de archivo sean EXACTOS a los de la carpeta media/profile_pics
    USUARIOS_FOTOS = {
        'Marcelo': 'marcelo_profile.jpg',
        'Ariadna': 'ariadna_profile.png',
        'Lonapoli': 'lonapoli.jpg',
        'Nicolas': 'nnapoli.jpg',
        'Federico': 'farias.jpg',
        # Agrega el resto si faltan
    }

    base_dir = 'media/profile_pics'

    print("--- INICIANDO REPARACIÓN Y CARGA ---")

    for username, filename in USUARIOS_FOTOS.items():
        try:
            # 1. Buscar usuario (sin importar mayúsculas/minúsculas en la búsqueda)
            user = User.objects.filter(username__iexact=username).first()
            
            if not user:
                print(f"❌ El usuario '{username}' no existe en la base de datos.")
                continue

            # 2. Obtener o CREAR el perfil (Aquí solucionamos el error)
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                print(f"   🔧 Perfil de {username} creado automáticamente.")

            # 3. Verificar archivo
            file_path = os.path.join(base_dir, filename)
            
            if os.path.exists(file_path):
                print(f"   Subiendo foto ({filename})...")
                with open(file_path, 'rb') as f:
                    profile.image.save(filename, File(f))
                print(f"✅ {username}: Foto actualizada.")
            else:
                print(f"⚠️  ARCHIVO FALTANTE: No encuentro '{file_path}' en el servidor.")
                print(f"    ¿Hiciste 'git add' de esa imagen?")

        except Exception as e:
            print(f"❌ Error crítico con {username}: {str(e)}")

    print("--- FIN ---")

if __name__ == '__main__':
    subir_imagenes()