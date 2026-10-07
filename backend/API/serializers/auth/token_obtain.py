from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from neomodel import DoesNotExist
from ...models import Utilisateur


class TokenObtain(TokenObtainPairSerializer):
    """
    Permet de se connecter avec pseudo / email + mot de passe.
    Retourne les tokens JWT (access, refresh) et lien utilisateur
    """

    def validate(self, attrs):
        request: HttpRequest = self.context.get("request")

        username: str = attrs.get("username")
        password: str = attrs.get("password")

        utilisateur: Utilisateur = authentification(username, password)

        refresh: RefreshToken = self.get_token(utilisateur)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "utilisateur": request.build_absolute_uri(
                reverse("utilisateur-detail", kwargs={"uuid": utilisateur.uuid})
            ),
        }


def authentification(username: str, password: str) -> Utilisateur:
    """Permet l'authentification d'un utilisateur

    Args:
        username (str): pseudo ou email de l'utilisateur
        password (str): mot de passe renseigner

    Raises:
        AuthenticationFailed: Échec de l'authentification

    Returns:
        Utilisateur: _description_
    """
    utilisateur: Utilisateur
    # Recherche par email ou pseudo
    # Test dans cette ordre à cause d'un défaut inérant à RegexProperty
    try:
        utilisateur = Utilisateur.nodes.get(pseudo=username)
    except DoesNotExist:
        try:
            utilisateur = Utilisateur.nodes.get(email=username)
        except:
            raise AuthenticationFailed("Identifiants invalides")

    # Vérification du mot de passe
    if check_password(password, utilisateur.password):
        return utilisateur
    else:
        raise AuthenticationFailed("Identifiants invalides")
