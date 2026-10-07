from typing import Any
from django.http import HttpRequest
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode, db
from neo4j.exceptions import ServiceUnavailable
from ...errors import NotFound, ConnexionDB
from ...serializers import BaseRelationShipSerializer
from . import BaseGenericViewSet


class BaseRelationShipViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    BaseGenericViewSet,
):
    """
    Classe de base pour les ModelViewSets des relations,
    contient les méthode de base pour les ViewSet de relationship

    Héritant de BaseGenericViewSet, CRUD incomplet par défaut pour les relations,
    d'où la différence avec les autres ViewSet héritant de ModelViewSet, pas de update ou de partial_update

    Champs additionnels :
        - router_lookup_field : nom du champ à récupérer dans l'url pour avoir le node de context
        - router_model_class : type de node du context du ViewSet
        - relationship : nom de la relation entre le node et le node de context
    """

    def __init__(
        self,
        serializer_class: Serializer,
        model_class: StructuredNode,
        router_lookup_field: str,
        router_model_class: StructuredNode,
        relationship: str,
        search_field: str = None,
        **kwargs,
    ):
        """
        ViewSet générique contenant toutes les méthodes pour les ViewSets enfants

        Args:
            serializer_class (Serializer): Serializer du ViewSet
            model_class (StructuredNode): type de node du ViewSet
            router_lookup_field (str): nom du champ à récupérer dans l'url pour avoir le node de context
            router_model_class (StructuredNode): type de node du context du ViewSet
            relationship (str): nom de la relation entre le node et le node de context
            search_field (str, optional): Champ utiliser pour la recherche si fourni. Defaults to None.
        """
        super().__init__(serializer_class, model_class, search_field, **kwargs)
        self.router_lookup_field: str = router_lookup_field
        self.router_model_class: StructuredNode = router_model_class
        self.relationship: str = relationship

    def get_nodeset(self) -> NodeSet:
        """
        Récupère le nodeset de la view,
        même chose qu'un queryset mais pour neomodel

        Raises:
            NotFound: Instance introuvable
            ConnexionDB: Base de données indisponible

        Returns:
            NodeSet: ensemble de StructuredNode du modèle
        """
        try:
            # Vérifie que l'instance du router existe bien
            self.get_context_model()
            return (
                super()
                .get_nodeset()
                .filter(
                    uuid__in=[
                        uuid[0]
                        for uuid in db.cypher_query(
                            # Requête CYPHER
                            f"MATCH (n:{self.model_class.__name__})-[:{self.relationship}]-\
                        (:{str(self.router_model_class.__name__)} "
                            + "{uuid: $uuid}) RETURN n.uuid",
                            {"uuid": self.kwargs[self.router_lookup_field]},
                        )[0]
                    ]
                )
            )
        except DoesNotExist:
            raise NotFound(self.router_model_class)
        # Dans le cas ou la base de données est inaccessible
        except ServiceUnavailable:  # pragma: no cover
            raise ConnexionDB()  # pragma: no cover

    def get_context_model(self) -> StructuredNode:
        """
        Récupère le node router pour le context

        Raises:
            NotFound: Instance introuvable
            ConnexionDB: Base de données indisponible

        Returns:
            StructuredNode: node du context
        """
        try:
            router_nodeset: NodeSet = self.router_model_class.nodes
            return router_nodeset.get(uuid=self.kwargs[self.router_lookup_field])
        # N'est jamais sensé passer pas ici, raise déjà dans get_nodeset
        except DoesNotExist:  # pragma: no cover
            raise NotFound(self.router_model_class)  # pragma: no cover
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable:  # pragma: no cover
            raise ConnexionDB()  # pragma: no cover

    def get_serializer_context(self) -> dict[str, Any]:
        """
        Modification du contexte du sérializer

        Returns:
            dict[str, Any]: context du Serializer
        """
        context = super().get_serializer_context()
        context_model_name: str = self.router_model_class.__name__
        context[context_model_name.lower()] = self.get_context_model()
        return context

    def perform_destroy(self, instance: StructuredNode):
        """
        Suppression de la RelationShip

        Args:
            instance (StructuredNode): instance à déconnecter
        """
        context_model_name: str = self.router_model_class.__name__
        serializer: BaseRelationShipSerializer = self.serializer_class(
            context={context_model_name.lower(): self.get_context_model()}
        )
        serializer.delete(instance.uuid)

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Création de la RelationShip

        Args:
            request (HttpRequest): requête pour la création

        Returns:
            Response: instance connecter
        """
        data: dict = request.data
        context_model_name: str = self.router_model_class.__name__
        serializer: BaseRelationShipSerializer = self.serializer_class(
            data=data, context={context_model_name.lower(): self.get_context_model()}
        )
        serializer.is_valid()
        instance: StructuredNode = serializer.create(serializer.validated_data)
        return Response(
            self.serializer_class(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )
