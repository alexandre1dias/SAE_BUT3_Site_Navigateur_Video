from rest_framework import serializers
from ..models import Extrait, Audio
from . import BaseRelationShipSerializer


class AudiosSerializer(BaseRelationShipSerializer):
    """
    Sérializer RelationShip audios (Extrait <-> Audio)

    Gestion des audios liés à un extrait

    Champs aditionnels :
        Relations :
            - audio : l'audio lié à l'extrait
            - extrait : les extraits liés à l'audio
        Champs en read_only :
            - name : nom de l'audio
    """

    # Outputs
    name = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Audio
        context_node : Extrait
        relation : audios
        """
        super().__init__(Audio, Extrait, "audios", *args, **kwargs)

    def get_extraits(self, audio: Audio):
        """
        Renvoie un lien propre vers les extraits
        """
        return self.get_url("extrait-list", kwargs={"audio_uuid": audio.uuid})
