from ..models import Extrait, Utilisateur
from ..serializers import RegarderExtraitsSerializer
from ..permissions import IsUserOrAdmin
from . import BaseRelationShipViewSet


class RegarderExtraitsViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les extraits regardés liés à un utilisateur, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les extraits regardés liés à un utilisateur:
    - GET /utilisateurs/{utilisateur_uuid}/regarder_extraits/ : Renvoie la liste de tous les extraits regardés liés à l'utilisateur avec l'uuid spécifié
    - GET /utilisateurs/{utilisateur_uuid}/regarder_extraits/{extrait_uuid}/ : Renvoie les détails de l'extrait regardé avec l'uuid spécifié lié à l'utilisateur avec l'uuid spécifié
    - POST /utilisateurs/{utilisateur_uuid}/regarder_extraits/ : Crée une nouvelle relation REGARDER_EXTRAITS entre extrait et utilisateur avec l'uuid spécifié
    - DELETE /utilisateurs/{utilisateur_uuid}/regarder_extraits/{extrait_uuid}/ : Supprime la relation REGARDER_EXTRAITS entre l'extrait avec l'uuid spécifié et l'utilisateur avec l'uuid spécifié

    permission_classes : IsUserOrAdmin (Seuls les utilisateurs eux-mêmes ou les administrateurs peuvent accéder à ces actions)
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Extrait lié à Utilisateur

        serializer : RegarderExtraitsSerializer
        node : Extrait
        router_lookup_field : utilisateur_uuid
        router_model_class : Utilisateur
        relationship : REGARDER_EXTRAITS
        search_field : title
        """
        super().__init__(
            RegarderExtraitsSerializer,
            Extrait,
            "utilisateur_uuid",
            Utilisateur,
            "REGARDER_EXTRAITS",
            "title",
            **kwargs
        )
