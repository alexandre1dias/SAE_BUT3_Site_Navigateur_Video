from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from neo4j.exceptions import ServiceUnavailable
from neomodel.exceptions import DoesNotExist
from .models import Utilisateur
from .errors import ConnexionDB


class Neo4jJWTAuthentication(JWTAuthentication):
    """
    Gestion de l'authentification avec Utilisateur
    N'utilise pas le système de user de Django par défaut
    Adaptation du système avec les utilisateurs du modèle Neo4j
    """

    def get_user(self, validated_token):
        user_id = validated_token.get("user_uuid")

        if not user_id:
            raise AuthenticationFailed("Token invalide")

        try:
            return Utilisateur.nodes.get(uuid=user_id)
        except DoesNotExist:
            raise AuthenticationFailed("Utilisateur introuvable")
        except ServiceUnavailable:
            raise ConnexionDB()
