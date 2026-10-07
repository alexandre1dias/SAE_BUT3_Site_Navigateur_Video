from ..models import Tag
from ..serializers import TagSerializer
from . import BaseModelViewSet


class TagViewSet(BaseModelViewSet):
    """
    ViewSet pour les tags, héritant de BaseModelViewSet

    CRUD complet pour les tags:
    - GET /tags/ : Renvoie la liste de tous les tags
    - GET /tags/{uuid}/ : Renvoie les détails du tag avec l'uuid spécifié
    - POST /tags/ : Crée un nouvel tag
    - PUT /tags/{uuid}/ : Met à jour le tag avec l'uuid spécifié
    - PATCH /tags/{uuid}/ : Met à jour partiellement le tag avec l'uuid spécifié
    - DELETE /tags/{uuid}/ : Supprime le tag avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Tag

        serializer : TagSerializer
        node : Tag
        """
        super().__init__(TagSerializer, Tag, **kwargs)
