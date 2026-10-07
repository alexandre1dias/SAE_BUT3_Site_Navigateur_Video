from ..models import Interview, Tag
from ..serializers import TagsInterviewRelationShipSerializer
from . import BaseRelationShipViewSet


class TagsInterviewRelationShipViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les tags liés à une interview, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les tags liés à une interview:
    - GET /interviews/{interview_uuid}/tags/ : Renvoie la liste de tous les tags liés à l'interview avec l'uuid spécifié
    - GET /interviews/{interview_uuid}/tags/{tag_uuid}/ : Renvoie les détails du tag avec l'uuid spécifié lié à l'interview avec l'uuid spécifié
    - POST /interviews/{interview_uuid}/tags/ : Crée une nouvelle relation TAGS_INTERVIEW entre tag et interview avec l'uuid spécifié
    - DELETE /interviews/{interview_uuid}/tags/{tag_uuid}/ : Supprime la relation TAGS_INTERVIEW entre le tag avec l'uuid spécifié et l'interview avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Tag lié à Interview

        serializer : TagsInterviewRelationShipSerializer
        node : Tag
        router_lookup_field : interview_uuid
        router_model_class : Interview
        relationship : TAGS_INTERVIEW
        """
        super().__init__(
            TagsInterviewRelationShipSerializer,
            Tag,
            "interview_uuid",
            Interview,
            "TAGS_INTERVIEW",
            **kwargs
        )
