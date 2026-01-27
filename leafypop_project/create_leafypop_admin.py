import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'leafypop'
password = 'LeafyPopSuperAdmin#2026'
email = 'info@leafypop.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"SUCCESS: Superuser '{username}' created successfully!")
    print(f"PASSWORD: {password}")
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"UPDATE: User '{username}' already existed. Password updated.")
    print(f"PASSWORD: {password}")
