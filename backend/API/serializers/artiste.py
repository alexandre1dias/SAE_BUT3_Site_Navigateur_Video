from rest_framework import serializers
from ..models import Artiste
from . import BaseSerializer


class ArtisteSerializer(BaseSerializer):
    """
    Sérializer du node Artiste

    Champs aditionnels :
        - name : nom de l'artiste (obligatoire)
        Relations :
            - extraits : les extraits liés à l'artiste
    """

    name = serializers.CharField(required=True)

    # Output
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Artiste
        """
        super().__init__(Artiste, *args, **kwargs)

    def get_extraits(self, artiste):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", {"artiste_uuid": artiste.uuid})
