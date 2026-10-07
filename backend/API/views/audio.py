from ..models import Audio
from ..serializers import AudioSerializer
from . import BaseModelViewSet


class AudioViewSet(BaseModelViewSet):
    """
    ViewSet pour les audios, héritant de BaseModelViewSet

    CRUD complet pour les audios:
    - GET /audios/ : Renvoie la liste de tous les audios
    - GET /audios/{uuid}/ : Renvoie les détails de l'audio avec l'uuid spécifié
    - POST /audios/ : Crée un nouvel audio
    - PUT /audios/{uuid}/ : Met à jour l'audio avec l'uuid spécifié
    - PATCH /audios/{uuid}/ : Met à jour partiellement l'audio avec l'uuid spécifié
    - DELETE /audios/{uuid}/ : Supprime l'audio avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Audio

        serializer : AudioSerializer
        node : Audio
        search_field : name
        """
        super().__init__(AudioSerializer, Audio, "name", **kwargs)
