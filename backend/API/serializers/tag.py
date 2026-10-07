from rest_framework import serializers
from ..models import Tag
from . import BaseSerializer


class TagSerializer(BaseSerializer):
    """
    Sérializer du node Tag

    Champs aditionnels :
        - name : nom du tag (obligatoire)
        Relations :
            - interviews : les interviews liées au tag
            - extraits : les extraits liés au tag
    """

    name = serializers.CharField(required=True)

    # Outputs
    interviews = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Tag
        """
        super().__init__(Tag, *args, **kwargs)

    def get_interviews(self, tag):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url("interview-list", kwargs={"tag_uuid": tag.uuid})

    def get_extraits(self, tag):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"tag_uuid": tag.uuid})
