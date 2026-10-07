from rest_framework import serializers
from ..models import Interview
from . import RelationShipUtilisateurSerializer


class RegarderInterviewsSerializer(RelationShipUtilisateurSerializer):
    """
    Sérializer RelationShip regarder_interviews (Utilisateur <-> Interview)

    Gestion des interviews liées à une recherche d'un utilisateur

    Champs aditionnels :
        Relations :
            - extraits : les extraits liés à l'interview
            - tags : les tags liés à l'interview
        Champs en read_only :
            - titre : titre de l'interview
            - date : date de l'interview
            - occasion : l'occasion de l'interview
            - description : description de l'interview
    """

    # Outputs
    titre = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    occasion = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Interview, "regarder_interviews", *args, **kwargs)

    def get_occasion(self, interview):
        """
        Renvoie un lien propre vers l'occasion
        """
        occasion = interview.occasion.single()
        return (
            self.get_url("occasion-detail", kwargs={"uuid": occasion.uuid})
            if occasion
            else None
        )

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
