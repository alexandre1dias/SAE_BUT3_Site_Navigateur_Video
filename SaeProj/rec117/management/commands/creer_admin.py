"""Crée le compte d'administration par défaut s'il n'existe encore aucun super-utilisateur.

Utilisé par lancer.sh / lancer.bat :   python manage.py creer_admin
Compte créé : admin / rec117  (à changer sur /admin/ si le site est mis en ligne)
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

IDENTIFIANT = 'admin'
MOT_DE_PASSE = 'rec117'


class Command(BaseCommand):
    help = "Crée le compte admin/rec117 s'il n'y a encore aucun super-utilisateur."

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Compte administrateur deja present.')
            return
        User.objects.create_superuser(IDENTIFIANT, '', MOT_DE_PASSE)
        self.stdout.write(f'Compte administrateur cree : {IDENTIFIANT} / {MOT_DE_PASSE}')
