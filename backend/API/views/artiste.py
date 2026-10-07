from ..models import Artiste
from ..serializers import ArtisteSerializer
from . import BaseModelViewSet


class ArtisteViewSet(BaseModelViewSet):
    """
    ViewSet pour les artistes, héritant de BaseModelViewSet

    CRUD complet pour les artistes:
    - GET /artistes/ : Renvoie la liste de tous les artistes
    - GET /artistes/{uuid}/ : Renvoie les détails de l'artiste avec l'uuid spécifié
    - POST /artistes/ : Crée un nouvel artiste
    - PUT /artistes/{uuid}/ : Met à jour l'artiste avec l'uuid spécifié
    - PATCH /artistes/{uuid}/ : Met à jour partiellement l'artiste avec l'uuid spécifié
    - DELETE /artistes/{uuid}/ : Supprime l'artiste avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Artiste

        serializer : ArtisteSerializer
        node : Artiste
        search_field : name
        """
        super().__init__(ArtisteSerializer, Artiste, "name", **kwargs)
