from ..models import Extrait, Tag
from ..serializers import TagsExtraitRelationShipSerializer
from . import BaseRelationShipViewSet


class TagsExtraitRelationShipViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les tags liés à un extrait, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les tags liés à un extrait:
    - GET /extraits/{extrait_uuid}/tags/ : Renvoie la liste de tous les tags liés à l'extrait avec l'uuid spécifié
    - GET /extraits/{extrait_uuid}/tags/{tag_uuid}/ : Renvoie les détails du tag avec l'uuid spécifié lié à l'extrait avec l'uuid spécifié
    - POST /extraits/{extrait_uuid}/tags/ : Crée une nouvelle relation TAGS_EXTRAIT entre tag et extrait avec l'uuid spécifié
    - DELETE /extraits/{extrait_uuid}/tags/{tag_uuid}/ : Supprime la relation TAGS_EXTRAIT entre le tag avec l'uuid spécifié et l'extrait avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Tag lié à Extrait

        serializer : TagsExtraitRelationShipSerializer
        node : Tag
        router_lookup_field : extrait_uuid
        router_model_class : Extrait
        relationship : TAGS_EXTRAIT
        """
        super().__init__(
            TagsExtraitRelationShipSerializer,
            Tag,
            "extrait_uuid",
            Extrait,
            "TAGS_EXTRAIT",
            **kwargs
        )
