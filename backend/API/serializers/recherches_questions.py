from rest_framework import serializers
from ..models import Question
from . import RelationShipUtilisateurSerializer


class RecherchesQuestionsSerializer(RelationShipUtilisateurSerializer):
    """
    Sérializer RelationShip recherches_questions (Utilisateur <-> Question)

    Gestion des questions liées à une recherche d'un utilisateur

    Champs aditionnels :
        Relations :
            - theme : le thème lié à la question
            - extraits : les extraits liés à la question
        Champs en read_only :
            - texte : texte de la question
    """

    # Outputs
    texte = serializers.CharField(read_only=True)
    theme = serializers.SerializerMethodField(read_only=True)
    extraits = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Question, "recherches_questions", *args, **kwargs)

    def get_theme(self, question):
        """
        Renvoie un lien propre vers le theme :
        """
        theme = question.theme.single()
        return (
            self.get_url("theme-detail", kwargs={"uuid": theme.uuid}) if theme else None
        )

    def get_extraits(self, question):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url("extrait-list", kwargs={"question_uuid": question.uuid})
