import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

print("=== DIAGNOSTICO DE IMAGENES ===")
for u in User.objects.all():
    try:
        p = u.profile
        name = p.image.name if p.image else "sin imagen"
        try:
            url = p.image.url if p.image else "sin url"
        except Exception as e:
            url = f"ERROR al generar URL: {e}"
        print(f"  {u.username}: name='{name}' | url='{url}'")
    except Exception as e:
        print(f"  {u.username}: SIN PERFIL ({e})")
print("=== FIN ===")
