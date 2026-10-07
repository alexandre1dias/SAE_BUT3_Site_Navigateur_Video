"""
Ensemble des classes Serializer utilisées pour la gestion de l'authentification

Classes :
    - TokenObtain : classe de sérializer pour l'obtention d'un token d'authentification
    - TokenRefresh : classe de sérializer pour le rafraîchissement d'un token d'authentification
"""

from .token_obtain import TokenObtain
from .token_refresh import TokenRefresh

__all__ = (
    "TokenObtain",
    "TokenRefresh",
)
