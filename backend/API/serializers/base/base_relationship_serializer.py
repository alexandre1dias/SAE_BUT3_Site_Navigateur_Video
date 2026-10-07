from rest_framework import serializers
from neomodel import StructuredNode, RelationshipManager, NodeSet
from neomodel.exceptions import DoesNotExist
from ...errors import ContextError, NotFound
from . import BaseSerializer


class BaseRelationShipSerializer(BaseSerializer):
    """
    Classe de base contenant les méthodes pour la gestion des relations entre les nodes de la base de données
        Afin d'avoir une gestion des champs write_only, utiliser pour créer des relations one-to-many,
        il faut ajouter dans la classe fille un dictionnaire input_fields de la forme :
        {"nom du champ du serializer": {"relationship": "attribut python relationship dans node", "node": Classe de node (model)}, }
    
    Champs :
        - uuid : uuid du node à relier (obligatoire)

    Raises:
        ContextError: node de context manquant
        NotFound: node non trouver
    """

    uuid = serializers.CharField(required=True)

    def __init__(
        self,
        node: StructuredNode,
        context_node: StructuredNode,
        relationship: str,
        *args,
        **kwargs
    ):
        """Création du Serializer de RelationShip

        Args:
            node (StructuredNode): type de node, on veut ajouter une relation avec une instance de cette classe
            context_node (StructuredNode): type de node, on veut ajouter une relation à partir de cette classe
            relationship (str): le nom de la relation entre node et context_node
        """
        super().__init__(node, *args, **kwargs)
        self.context_node = context_node
        self.relationship = relationship

    def create(self, validated_data) -> StructuredNode:
        """Création d'une relation entre les deux nodes

        Args:
            validated_data (dict): Les données permettant de créer la relation

        Raises:
            ContextError: node de context manquant
            NotFound: node non trouver

        Returns:
            StructuredNode: node ajouter aux relations du node de context
        """
        context: StructuredNode = self.context.get(self.context_node.__name__.lower())
        if not context:
            raise ContextError(self.context_node)
        try:
            nodeset: NodeSet = self.node.nodes
            instance: StructuredNode = nodeset.get(
                uuid=validated_data.pop("uuid", None)
            )
        except DoesNotExist:
            raise NotFound(self.node)
        relationship: RelationshipManager = getattr(context, self.relationship)
        if not relationship.is_connected(instance):
            if validated_data:
                relationship.connect(instance, validated_data)
            else:
                relationship.connect(instance)
        return instance

    def delete(self, uuid) -> StructuredNode:
        """Suppression d'une relation entre le node de context et le node fourni

        Args:
            uuid (str): uuid du node à déconnecter du node de context

        Raises:
            ContextError: node de context manquant
            NotFound: node non trouver

        Returns:
            StructuredNode: node déconnecter des relations du node de context
        """
        context_node: StructuredNode = self.context.get(
            str(self.context_node.__name__).lower()
        )
        if not context_node:
            raise ContextError(self.context_node)
        try:
            nodeset: NodeSet = self.node.nodes
            instance: StructuredNode = nodeset.get(uuid=uuid)
        except DoesNotExist:
            raise NotFound(self.node)
        relationship: RelationshipManager = getattr(context_node, self.relationship)
        relationship.disconnect(instance)
        return instance
