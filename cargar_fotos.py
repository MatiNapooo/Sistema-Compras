import os
import django

# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files import File

def subir_imagenes():
    # --- CONFIGURACIÓN: ASOCIA USUARIO CON SU FOTO ---
    # Formato: 'nombre_de_usuario_django': 'nombre_archivo.jpg'
    USUARIOS_FOTOS = {
        'Marcelo': 'marcelo_profile.jpg',       # Ejemplo: Al usuario 'admin' le ponemos anorak.jpg
        'Ariadna': 'ariadna_profile.jpg',        # Cambia 'juan' por el usuario real
        'Lonapoli': 'lonapoli.jpg',
        'Nicolas': 'nnapoli.jpg',
        'Federico': 'farias.jpg',
    }

    base_dir = 'media/profile_pics'

    print("--- INICIANDO CARGA A CLOUDINARY ---")

    for username, filename in USUARIOS_FOTOS.items():
        try:
            # Buscamos al usuario
            user = User.objects.get(username=username)
            file_path = os.path.join(base_dir, filename)

            # Verificamos si el archivo existe en el proyecto
            if os.path.exists(file_path):
                print(f"Subiendo foto para {username} ({filename})...")
                
                # Abrimos el archivo y lo guardamos en el perfil
                with open(file_path, 'rb') as f:
                    # Al hacer .save(), Cloudinary intercepta y sube la foto a la nube
                    user.profile.image.save(filename, File(f))
                
                print(f"✅ Listo: {username}")
            else:
                print(f"⚠️  No encontré el archivo: {file_path}")

        except User.DoesNotExist:
            print(f"❌ El usuario '{username}' no existe en la base de datos.")
        except Exception as e:
            print(f"❌ Error con {username}: {str(e)}")

    print("--- FIN ---")

if __name__ == '__main__':
    subir_imagenes()