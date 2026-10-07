from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from neomodel import StructuredNode
from . import BaseGenericViewSet


class BaseModelViewSet(BaseGenericViewSet, ModelViewSet):
    """
    Classe de base pour les ModelViewSets classiques, héritant de BaseGenericViewSet

    CRUD complet par défaut pour les endpoints, pas de champs additionnels

    Champs :
        - lookup_field : champ utilisé pour la recherche d'une instance
    """

    def __init__(
        self,
        serializer_class: Serializer,
        model_class: StructuredNode,
        search_field: str = None,
        **kwargs
    ):
        """
        ViewSet générique contenant toutes les méthodes pour les ViewSets enfants

        Args:
            serializer_class (Serializer): Serializer du ViewSet
            model_class (StructuredNode): type de node du ViewSet
            search_field (str, optional): Champ utiliser pour la recherche si fourni. Defaults to None.
        """
        super().__init__(serializer_class, model_class, search_field, **kwargs)
