from ..models import Artiste, Utilisateur
from ..serializers import RecherchesArtistesSerializer
from ..permissions import IsUserOrAdmin
from . import BaseRelationShipViewSet


class RecherchesArtistesViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les recherches d'artistes liées à un utilisateur, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les recherches d'artistes liées à un utilisateur:
    - GET /utilisateurs/{utilisateur_uuid}/recherches_artistes/ : Renvoie la liste de tous les artistes recherchés liés à l'utilisateur avec l'uuid spécifié
    - GET /utilisateurs/{utilisateur_uuid}/recherches_artistes/{artiste_uuid}/ : Renvoie les détails de l'artiste recherché avec l'uuid spécifié lié à l'utilisateur avec l'uuid spécifié
    - POST /utilisateurs/{utilisateur_uuid}/recherches_artistes/ : Crée une nouvelle relation RECHERCHES_ARTISTES entre artiste et utilisateur avec l'uuid spécifié
    - DELETE /utilisateurs/{utilisateur_uuid}/recherches_artistes/{artiste_uuid}/ : Supprime la relation RECHERCHES_ARTISTES entre l'artiste avec l'uuid spécifié et l'utilisateur avec l'uuid spécifié

    permission_classes : IsUserOrAdmin (Seuls les utilisateurs eux-mêmes ou les administrateurs peuvent accéder à ces actions)
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Artiste lié à Utilisateur

        serializer : RecherchesArtistesSerializer
        node : Artiste
        router_lookup_field : utilisateur_uuid
        router_model_class : Utilisateur
        relationship : RECHERCHES_ARTISTES
        search_field : name
        """
        super().__init__(
            RecherchesArtistesSerializer,
            Artiste,
            "utilisateur_uuid",
            Utilisateur,
            "RECHERCHES_ARTISTES",
            "name",
            **kwargs
        )
