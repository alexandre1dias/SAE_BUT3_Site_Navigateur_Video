from ..models import Audio, Extrait
from ..serializers import AudiosSerializer
from . import BaseRelationShipViewSet


class AudiosViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les audios liés à un extrait, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les audios liés à un extrait:
    - GET /extraits/{extrait_uuid}/audios/ : Renvoie la liste de tous les audios liés à l'extrait avec l'uuid spécifié
    - GET /extraits/{extrait_uuid}/audios/{audio_uuid}/ : Renvoie les détails de l'audio avec l'uuid spécifié lié à l'extrait avec l'uuid spécifié
    - POST /extraits/{extrait_uuid}/audios/ : Crée une nouvelle relation AUDIOS entre audio et extrait avec l'uuid spécifié
    - DELETE /extraits/{extrait_uuid}/audios/{audio_uuid}/ : Supprime la relation AUDIOS entre l'audio avec l'uuid spécifié et l'extrait avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Audio lié à Extrait

        serializer : AudiosSerializer
        node : Audio
        router_lookup_field : extrait_uuid
        router_lookup_url_kwarg : extrait_uuid
        router_model_class : Extrait
        relationship : AUDIOS
        search_field : name
        """
        super().__init__(
            AudiosSerializer,
            Audio,
            "extrait_uuid",
            Extrait,
            "AUDIOS",
            "name",
            **kwargs
        )