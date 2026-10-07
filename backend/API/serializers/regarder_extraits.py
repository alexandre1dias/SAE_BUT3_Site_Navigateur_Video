from rest_framework import serializers
from ..models import Extrait
from . import RelationShipUtilisateurSerializer


class RegarderExtraitsSerializer(RelationShipUtilisateurSerializer):
    """
    Sérializer RelationShip regarder_extraits (Utilisateur <-> Extrait)

    Gestion des extraits liés à une recherche d'un utilisateur

    Champs aditionnels :
        Relations :
            - artiste : l'artiste lié à l'extrait
            - question : la question liée à l'extrait
            - interviews : les interviews liées à l'extrait
            - audios : les audios liés à l'extrait
            - tags : les tags liés à l'extrait
        Champs en read_only :
            - titre : titre de l'extrait
            - description : description de l'extrait
            - youtube_url : url de la vidéo youtube de l'extrait
            - vimeo_url : url de la vidéo vimeo de l'extrait
            - lieu : lieu de l'extrait
            - uploaded_at : date de mise en ligne de l'extrait
            - duree : durée de l'extrait en secondes
    """

    # Outputs
    titre = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    youtube_url = serializers.CharField(read_only=True)
    vimeo_url = serializers.CharField(read_only=True)
    lieu = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateField(read_only=True)
    duree = serializers.IntegerField(read_only=True)
    artiste = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    audios = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(Extrait, "regarder_extraits", *args, **kwargs)

    def get_artiste(self, extrait):
        """
        Renvoie un lien propre vers l'artiste :
        """
        artiste = extrait.interviewer.single()
        return (
            self.get_url("artiste-detail", kwargs={"uuid": artiste.uuid})
            if artiste
            else None
        )

    def get_question(self, extrait):
        """
        Renvoie un lien propre vers la question :
        """
        question = extrait.question.single()
        return (
            self.get_url("question-detail", kwargs={"uuid": question.uuid})
            if question
            else None
        )

    def get_interviews(self, extrait):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url("interview-list", kwargs={"extrait_uuid": extrait.uuid})

    def get_audios(self, extrait: Extrait):
        """Renvoie un lien vers les audios

        Args:
            extrait (Extrait): un extrait
        """
        return self.get_url("audio-list", kwargs={"extrait_uuid": extrait.uuid})

    def get_tags(self, extrait):
        """
        Renvoie un lien propre vers les tags :
        """
        return self.get_url("tag-list", kwargs={"extrait_uuid": extrait.uuid})
