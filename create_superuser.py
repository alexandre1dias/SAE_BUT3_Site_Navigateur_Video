import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lecteurMap.settings") 
django.setup()

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    print(f"Création du superutilisateur {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("Le superutilisateur existe déjà.")
