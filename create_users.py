import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

users_data = [
    {'username': 'nnapoli', 'password': 'npsa1141', 'first_name': 'Nicolas'},
    {'username': 'lonapoli', 'password': 'catapipa', 'first_name': 'Luis'},
    {'username': 'Farias', 'password': 'pitochico', 'first_name': 'Federico'},
    {'username': 'Anorak', 'password': 'perzival', 'first_name': 'Matias'},
]

for data in users_data:
    user, created = User.objects.get_or_create(username=data['username'])
    user.set_password(data['password'])
    user.first_name = data['first_name']
    user.save()
    
    # Create profile if not exists
    Profile.objects.get_or_create(user=user)
    
    if created:
        print(f"Usuario creado: {data['username']}")
    else:
        print(f"Usuario actualizado: {data['username']}")

print("Proceso finalizado.")
