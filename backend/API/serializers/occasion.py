from rest_framework import serializers
from ..models import Occasion
from . import BaseSerializer


class OccasionSerializer(BaseSerializer):
    """
    Sérializer du node Occasion

    Champs aditionnels :
        - name : nom de l'occasion (obligatoire)
        Relations :
            - interviews : les interviews liées à l'occasion
    """

    name = serializers.CharField(required=True)

    # Output
    interviews = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Occasion
        """
        super().__init__(Occasion, *args, **kwargs)

    def get_interviews(self, occasion: Occasion):
        """
        Renvoie un lien propre vers les interviews
        """
        return self.get_url("interview-list", kwargs={"occasion_uuid": occasion.uuid})
