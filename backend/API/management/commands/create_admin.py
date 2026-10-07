from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from neomodel import db
from ...models import Utilisateur


class Command(BaseCommand):
    """
    Commande pour créer un utilisateur administrateur

    args:
        - pseudo : str
        - password : str
        - email : str
    """
    
    help = "Créer un utilisateur administrateur"

    def add_arguments(self, parser):
        parser.add_argument("pseudo", type=str, help="Pseudo de l'utilisateur")
        parser.add_argument("password", type=str, help="Mot de passe")
        parser.add_argument("email", type=str, help="Adresse email")

    def handle(self, *args, **options):
        pseudo = options["pseudo"]
        password = options["password"]
        email = options["email"]

        try:
            user = Utilisateur(
                pseudo=pseudo,
                email=email,
                password=make_password(password),
                prenom="Admin",
                nom="Admin",
                is_admin=True
            ).save()

            self.stdout.write(
                self.style.SUCCESS(f"Ajout de l'administrateur {user}")
            )

        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f"Échec de l'ajout de l'administrateur :\n{error}")
            )
