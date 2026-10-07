from ..models import Extrait
from . import RelationShipTagSerializer


class TagsExtraitRelationShipSerializer(RelationShipTagSerializer):
    """
    Sérializer RelationShip tags_extrait (Extrait <-> Tag)

    Gestion des tags liés à un extrait
    """

    def __init__(self, *args, **kwargs):
        """
        node : Tag
        context_node : Extrait
        relation : tags_extrait
        """
        super().__init__(Extrait, "tags_extrait", *args, **kwargs)
