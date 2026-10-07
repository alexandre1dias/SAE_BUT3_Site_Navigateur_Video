from rest_framework import serializers
from ..models import Interview, Occasion
from . import BaseSerializer


class InterviewSerializer(BaseSerializer):
    """
    Sérializer du node Interview

    Champs aditionnels :
        - titre : titre de l'interview
        - date : date de l'interview
        - description : description de l'interview
        Relations :
            - occasion : l'occasion liée à l'interview
            - extraits : les extraits liés à l'interview
            - tags : les tags liés à l'interview
    """

    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    # Input
    input_fields = {"occasion_uuid": {"relationship": "occasion", "node": Occasion}}
    occasion_uuid = serializers.CharField(
        write_only=True,
        required=False,
    )

    # Outputs
    occasion = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Interview
        """
        super().__init__(Interview, *args, **kwargs)

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
