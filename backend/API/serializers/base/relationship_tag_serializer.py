from rest_framework import serializers
from neomodel import StructuredNode
from ...models import Tag
from . import BaseRelationShipSerializer


class RelationShipTagSerializer(BaseRelationShipSerializer):
    """
    Classe de base contenant les méthodes pour la gestion des relations concernant les tags

    Gestion des tags liés à un extrait ou une interview

    Champs aditionnels :
        Relations :
            - interviews : les interviews liées au tag
            - extraits : les extraits liés au tag
        Champs en read_only :
            - name : nom du tag
    """

    name = serializers.CharField(read_only=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(
        self, context_node: StructuredNode, relationship: str, *args, **kwargs
    ):
        """Création du Serializer de RelationShip concernant les tags

        Args:
            context_node (StructuredNode): type de node, ayant un type de relationship existante avec Tag
            relationship (str): le nom de la relation entre Tag et context_node

            node : Tag
        """
        super().__init__(Tag, context_node, relationship, *args, **kwargs)

    def get_interviews(self, tag: Tag) -> str:
        """Renvoie un lien propre vers les interviews d'un tag

        Args:
            tag (Tag): instance de Tag

        Returns:
            str: url absolue pour obtenir les interviews liées au tag
        """
        return self.get_url("interview-list", kwargs={"tag_uuid": tag.uuid})

    def get_extraits(self, tag: Tag):
        """Renvoie un lien propre vers les extraits d'un tag

        Args:
            tag (Tag): instance de Tag

        Returns:
            str: url absolue pour obtenir les extraits liées au tag
        """
        return self.get_url("extrait-list", kwargs={"tag_uuid": tag.uuid})
