from rest_framework import serializers
from ..models import Audio
from . import BaseSerializer


class AudioSerializer(BaseSerializer):
    """
    Sérializer du node Audio

    Champs aditionnels :
        - name : nom de l'audio (obligatoire)
        Relations :
            - extraits : les extraits liés à l'audio
    """

    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Outputs
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Audio
        """
        super().__init__(Audio, *args, **kwargs)

    def get_extraits(self, audio):
        """
        Renvoie un lien propre vers les extraits
        """
        return self.get_url("extrait-list", kwargs={"audio_uuid": audio.uuid})
