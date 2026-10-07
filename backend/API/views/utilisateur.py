from rest_framework.permissions import AllowAny
from ..models import Utilisateur
from ..serializers import UtilisateurSerializer
from ..permissions import IsUserOrAdmin
from . import BaseModelViewSet


class UtilisateurViewSet(BaseModelViewSet):
    """
    ViewSet pour les utilisateurs, héritant de BaseModelViewSet

    CRUD complet pour les utilisateurs:
    - GET /utilisateurs/ : Renvoie la liste de tous les utilisateurs
    - GET /utilisateurs/{uuid}/ : Renvoie les détails de l'utilisateur avec l'uuid spécifié
    - POST /utilisateurs/ : Crée un nouvel utilisateur
    - PUT /utilisateurs/{uuid}/ : Met à jour l'utilisateur avec l'uuid spécifié
    - PATCH /utilisateurs/{uuid}/ : Met à jour partiellement l'utilisateur avec l'uuid spécifié
    - DELETE /utilisateurs/{uuid}/ : Supprime l'utilisateur avec l'uuid spécifié
    """

    # permission_classes = [IsUserOrAdmin]

    def get_permissions(self):
        """
        Permissions pour les utilisateurs

        - Seuls les utilisateurs eux-mêmes ou les administrateurs peuvent accéder aux actions de liste, de récupération, de mise à jour et de suppression
        - Tout le monde peut accéder à l'action de création d'utilisateur
        """
        if self.action in ["list", "retrieve", "update", "destroy"]:
            return [IsUserOrAdmin()]
        return [AllowAny()]

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Utilisateur

        serializer : UtilisateurSerializer
        node : Utilisateur
        """
        super().__init__(UtilisateurSerializer, Utilisateur, **kwargs)
