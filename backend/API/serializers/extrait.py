from rest_framework import serializers
from neomodel import db, StructuredNode
from ..errors import ValidatorUnique
from ..models import Artiste, Audio, Extrait, Question
from . import BaseSerializer


class ExtraitSerializer(BaseSerializer):
    """
    Sérializer du node Extrait

    Champs aditionnels :
        - titre : titre de l'extrait
        - description : description de l'extrait
        - youtube_url : url de la vidéo youtube de l'extrait
        - vimeo_url : url de la vidéo vimeo de l'extrait
        - lieu : lieu de l'extrait
        - uploaded_at : date de mise en ligne de l'extrait
        - duree : durée de l'extrait en secondes
        Relations :
            - artiste : l'artiste lié à l'extrait
            - question : la question liée à l'extrait
            - interviews : les interviews liées à l'extrait
            - audios : les audios liés à l'extrait
            - tags : les tags liés à l'extrait
    """

    titre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    youtube_url = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    vimeo_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lieu = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    uploaded_at = serializers.DateField(required=False, allow_null=True)
    duree = serializers.IntegerField(required=True)

    # Input:
    input_fields = {
        "artiste_uuid": {"relationship": "interviewer", "node": Artiste},
        "question_uuid": {"relationship": "question", "node": Question},
        "audio_uuid": {"relationship": "audios", "node": Audio},
    }
    artiste_uuid = serializers.CharField(write_only=True, required=False)
    question_uuid = serializers.CharField(write_only=True, required=False)
    audio_uuid = serializers.CharField(write_only=True, required=False)

    # Output:
    artiste = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    interviews = serializers.SerializerMethodField(read_only=True)
    audios = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    position = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Extrait

        Retire le champ `position` si aucune interview n'est dans le contexte.
        """
        super().__init__(Extrait, *args, **kwargs)

        # Champ position uniquement pertinent dans le contexte d'une interview, on le retire sinon
        if not self.context.get("interview"):
            self.fields.pop("position", None)

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

    def get_position(self, extrait):
        interview = self.context.get("interview")
        return int(
            db.cypher_query(
                "MATCH (e:Extrait {uuid:$extrait_uuid})-[r:APPARTIENT_A]->(i:Interview {uuid:$interview_uuid}) RETURN r.position AS pos",
                {"extrait_uuid": extrait.uuid, "interview_uuid": interview.uuid},
            )[0][0][0]
        )

    def create(self, validated_data: dict) -> StructuredNode:
        """
        Avant la création d'un extrait, on vérifie que les liens yt et vimeo ne sont pas déjà présent dans la bd

        Args:
            validated_data (dict): Les données permettant de créer la relation

        Raises:
            ValidatorUnique: url déjà présent

        Returns:
            StructuredNode: node ajouter aux relations du node de context
        """
        youtube_url = validated_data.get("youtube_url", None)
        vimeo_url = validated_data.get("vimeo_utl", None)
        node = None

        if youtube_url:
            try:
                node = Extrait.nodes.get(youtube_url=youtube_url)
                raise ValidatorUnique("youtube_url")
            except ValidatorUnique as e:
                raise e
            except:
                pass

        elif not node:
            try:
                node = Extrait.nodes.get(vimeo_url=vimeo_url)
                raise ValidatorUnique("vimeo_url")
            except ValidatorUnique as e:
                raise e
            except:
                pass

        return super().create(validated_data)
