from ..models import Occasion
from ..serializers import OccasionSerializer
from . import BaseModelViewSet


class OccasionViewSet(BaseModelViewSet):
    """
    ViewSet pour les occasions, héritant de BaseModelViewSet

    CRUD complet pour les occasions:
    - GET /occasions/ : Renvoie la liste de tous les occasions
    - GET /occasions/{uuid}/ : Renvoie les détails de l'occasion avec l'uuid spécifié
    - POST /occasions/ : Crée un nouvel occasion
    - PUT /occasions/{uuid}/ : Met à jour l'occasion avec l'uuid spécifié
    - PATCH /occasions/{uuid}/ : Met à jour partiellement l'occasion avec l'uuid spécifié
    - DELETE /occasions/{uuid}/ : Supprime l'occasion avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Occasion

        serializer : OccasionSerializer
        node : Occasion
        search_field : name
        """
        super().__init__(OccasionSerializer, Occasion, "name", **kwargs)
