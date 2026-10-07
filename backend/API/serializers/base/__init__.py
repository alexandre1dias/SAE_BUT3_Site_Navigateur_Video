"""
Ensemble des classes Serializer contenant les méthodes génériques utilisé par leurs classes enfants

Classes :
    - BaseSerializer : classe de base contenant les méthodes pour la gestion des données (node)
    - BaseRelationShipSerializer : classe de base contenant les méthodes pour la gestion des relations entre les nodes de la base de données
    - RelationShipUtilisateurSerializer : classe de base contenant les méthodes pour la gestion des relations concernant les utilisateurs
    - RelationShipTagSerializer : classe de base contenant les méthodes pour la gestion des relations concernant les tags
"""

from .base_serializer import BaseSerializer
from .base_relationship_serializer import BaseRelationShipSerializer
from .relationship_utilisateur_serializer import RelationShipUtilisateurSerializer
from .relationship_tag_serializer import RelationShipTagSerializer

__all__ = (
    "BaseSerializer",
    "BaseRelationShipSerializer",
    "RelationShipUtilisateurSerializer",
    "RelationShipTagSerializer",
)
