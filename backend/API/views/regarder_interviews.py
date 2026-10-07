from ..models import Interview, Utilisateur
from ..serializers import RegarderInterviewsSerializer
from ..permissions import IsUserOrAdmin
from . import BaseRelationShipViewSet


class RegarderInterviewsViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les interviews regardées liées à un utilisateur, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les interviews regardées liées à un utilisateur:
    - GET /utilisateurs/{utilisateur_uuid}/regarder_interviews/ : Renvoie la liste de tous les interviews regardés liés à l'utilisateur avec l'uuid spécifié
    - GET /utilisateurs/{utilisateur_uuid}/regarder_interviews/{interview_uuid}/ : Renvoie les détails de l'interview regardé avec l'uuid spécifié lié à l'utilisateur avec l'uuid spécifié
    - POST /utilisateurs/{utilisateur_uuid}/regarder_interviews/ : Crée une nouvelle relation REGARDER_INTERVIEWS entre interview et utilisateur avec l'uuid spécifié
    - DELETE /utilisateurs/{utilisateur_uuid}/regarder_interviews/{interview_uuid}/ : Supprime la relation REGARDER_INTERVIEWS entre l'interview avec l'uuid spécifié et l'utilisateur avec l'uuid spécifié

    permission_classes : IsUserOrAdmin (Seuls les utilisateurs eux-mêmes ou les administrateurs peuvent accéder à ces actions)
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Interview lié à Utilisateur

        serializer : RegarderInterviewsSerializer
        node : Interview
        router_lookup_field : utilisateur_uuid
        router_model_class : Utilisateur
        relationship : REGARDER_INTERVIEWS
        search_field : title
        """
        super().__init__(
            RegarderInterviewsSerializer,
            Interview,
            "utilisateur_uuid",
            Utilisateur,
            "REGARDER_INTERVIEWS",
            "title",
            **kwargs
        )
