import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_project.settings')
django.setup()

from django.contrib.auth.models import User
# Profile is automatically created via signals usually, but we are updating existing ones

def update_profile(username_part, image_path):
    try:
        user = User.objects.filter(username__icontains=username_part).first()
        if user:
            print(f"Found user: {user.username}")
            # Ensure profile exists
            if not hasattr(user, 'profile'):
                from core.models import Profile
                Profile.objects.create(user=user)
            
            user.profile.image = image_path
            user.profile.save()
            print(f"Updated profile image for {user.username} to {image_path}")
        else:
            print(f"User with username containing '{username_part}' not found.")
            # Check all users
            print("Available users:", [u.username for u in User.objects.all()])
    except Exception as e:
        print(f"Error updating {username_part}: {e}")

if __name__ == '__main__':
    update_profile('marcelo', 'profile_pics/marcelo_profile.jpg')
    update_profile('aridna', 'profile_pics/ariadna_profile.png')
