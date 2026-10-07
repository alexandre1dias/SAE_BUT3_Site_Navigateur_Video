from rest_framework import serializers
from ..models import Extrait, Interview
from . import BaseRelationShipSerializer


class InterviewsSerializer(BaseRelationShipSerializer):
    """
    Sérializer RelationShip interviews (Extrait <-> Interview)

    Gestion des interviews liées à un extrait

    Champs aditionnels :
        - position : position de l'extrait dans l'interview (obligatoire)
        Relations :
            - extraits : les extraits liés à l'interview
            - tags : les tags liés à l'interview
        Champs en read_only :
            - titre : titre de l'interview
            - date : date de l'interview
            - occasion : l'occasion de l'interview
            - description : description de l'interview
    """

    position = serializers.IntegerField(write_only=True, required=True)

    # Outputs
    titre = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    occasion = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Interview
        context_node : Extrait
        relation : interviews
        """
        super().__init__(Interview, Extrait, "interviews", *args, **kwargs)

    def get_extraits(self, interview):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"interview_uuid": interview.uuid})

    def get_tags(self, interview):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url("tag-list", kwargs={"interview_uuid": interview.uuid})


class PositionInputSerializer(serializers.Serializer):
    """
    Sérializer RelationShip interviews (Extrait <-> Interview) update
    """

    position = serializers.IntegerField(write_only=True, required=True)
