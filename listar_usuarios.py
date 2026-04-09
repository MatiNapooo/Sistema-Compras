import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()
from django.contrib.auth.models import User
from core.models import Profile
print("=== USUARIOS EN DB ===")
for u in User.objects.all():
    try:
        img = u.profile.image.name if u.profile.image else "sin imagen"
    except:
        img = "sin perfil"
    print(f"  username='{u.username}' | first_name='{u.first_name}' | imagen='{img}'")
print(f"Total: {User.objects.count()} usuarios")
