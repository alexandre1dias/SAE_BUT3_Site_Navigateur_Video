from rest_framework import serializers
from ..models import Theme
from . import BaseSerializer


class ThemeSerializer(BaseSerializer):
    """
    Sérializer du node Theme

    Champs aditionnels :
        - name : nom du thème (obligatoire)
        Relations :
            - questions : les questions liées au thème
    """

    name = serializers.CharField(required=True)

    # Outputs
    questions = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Theme
        """
        super().__init__(Theme, *args, **kwargs)

    def get_questions(self, theme):
        """
        Renvoie un lien propre vers les questions :
        """
        return self.get_url("question-list", kwargs={"theme_uuid": theme.uuid})
