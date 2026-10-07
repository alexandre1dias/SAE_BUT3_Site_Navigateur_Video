"""
Ensemble des classes ViewSet contenant les méthodes génériques utilisé par leurs classes enfants

Classes :
    - BaseGenericViewSet : ViewSet générique de base
    - BaseModelViewSet : ViewSet de base pour les modèles
    - SubBaseModelViewSet : ViewSet de base pour les modèles enfants
    - BaseRelationShipViewSet : ViewSet de base pour les relations entre modèles
"""

from .base_generic import BaseGenericViewSet
from .base_viewset import BaseModelViewSet
from .sub_base_viewset import SubBaseModelViewSet
from .base_relationship_viewset import BaseRelationShipViewSet

__all__ = (
    "BaseGenericViewSet",
    "BaseModelViewSet",
    "SubBaseModelViewSet",
    "BaseRelationShipViewSet",
)
