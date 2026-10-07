from ..models import Theme
from ..serializers import ThemeSerializer
from . import BaseModelViewSet


class ThemeViewSet(BaseModelViewSet):
    """
    ViewSet pour les thèmes, héritant de BaseModelViewSet

    CRUD complet pour les thèmes:
    - GET /themes/ : Renvoie la liste de tous les thèmes
    - GET /themes/{uuid}/ : Renvoie les détails du thème avec l'uuid spécifié
    - POST /themes/ : Crée un nouvel thème
    - PUT /themes/{uuid}/ : Met à jour le thème avec l'uuid spécifié
    - PATCH /themes/{uuid}/ : Met à jour partiellement le thème avec l'uuid spécifié
    - DELETE /themes/{uuid}/ : Supprime le thème avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Theme

        serializer : ThemeSerializer
        node : Theme
        """
        super().__init__(ThemeSerializer, Theme, **kwargs)
