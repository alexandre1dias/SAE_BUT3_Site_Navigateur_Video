from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet
from neomodel import StructuredNode
from neo4j.exceptions import ServiceUnavailable
from ..models import Artiste, Audio, Extrait, Interview, Question, Tag
from ..serializers import ExtraitSerializer
from ..errors import ConnexionDB, NotFound
from . import BaseModelViewSet, SubBaseModelViewSet


class ExtraitViewSet(BaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de BaseModelViewSet

    CRUD complet pour les extraits:
    - GET /extraits/ : Renvoie la liste de tous les extraits
    - GET /extraits/{uuid}/ : Renvoie les détails de l'extrait avec l'uuid spécifié
    - POST /extraits/ : Crée un nouvel extrait
    - PUT /extraits/{uuid}/ : Met à jour l'extrait avec l'uuid spécifié
    - PATCH /extraits/{uuid}/ : Met à jour partiellement l'extrait avec l'uuid spécifié
    - DELETE /extraits/{uuid}/ : Supprime l'extrait avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Extrait

        serializer : ExtraitSerializer
        node : Extrait
        search_field : titre
        """
        super().__init__(ExtraitSerializer, Extrait, "titre", **kwargs)


class QuestionExtraitViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'une question:
    - GET /questions/{question_uuid}/extraits/ : Renvoie la liste de tous les extraits liés à la question avec l'uuid spécifié
    - GET /questions/{question_uuid}/extraits/{uuid}/ : Renvoie les détails de l'extrait avec l'uuid spécifié lié à la question avec l'uuid spécifié
    - POST /questions/{question_uuid}/extraits/ : Crée un nouvel extrait non lié à une question par défaut, création d'un extrait classique
    - PUT /questions/{question_uuid}/extraits/{uuid}/ : Met à jour l'extrait avec l'uuid spécifié lié à la question avec l'uuid spécifié
    - PATCH /questions/{question_uuid}/extraits/{uuid}/ : Met à jour partiellement l'extrait avec l'uuid spécifié lié à la question avec l'uuid spécifié
    - DELETE /questions/{question_uuid}/extraits/{uuid}/ : Supprime l'extrait avec l'uuid spécifié lié à la question avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Extrait en fonction d'un node Question

        serializer : ExtraitSerializer
        node : Extrait
        router_lookup_field : question_uuid
        router_model_class : Question
        relationship : POSE
        search_field : titre
        """
        super().__init__(
            ExtraitSerializer,
            Extrait,
            "question_uuid",
            Question,
            "POSE",
            "titre",
            **kwargs
        )


class InterviewExtraitViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'une interview:
    - GET /interviews/{interview_uuid}/extraits/ : Renvoie la liste de tous les extraits liés à l'interview avec l'uuid spécifié ordonnés par ordre de position dans l'interview
    - GET /interviews/{interview_uuid}/extraits/{uuid}/ : Renvoie les détails de l'extrait avec l'uuid spécifié lié à l'interview avec l'uuid spécifié
    - POST /interviews/{interview_uuid}/extraits/ : Crée un nouvel extrait non lié à une interview par défaut, création d'un extrait classique
    - PUT /interviews/{interview_uuid}/extraits/{uuid}/ : Met à jour l'extrait avec l'uuid spécifié lié à l'interview avec l'uuid spécifié
    - PATCH /interviews/{interview_uuid}/extraits/{uuid}/ : Met à jour partiellement l'extrait avec l'uuid spécifié lié à l'interview avec l'uuid spécifié
    - DELETE /interviews/{interview_uuid}/extraits/{uuid}/ : Supprime l'extrait avec l'uuid spécifié lié à l'interview avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Extrait en fonction d'un node Interview

        serializer : ExtraitSerializer
        node : Extrait
        router_lookup_field : interview_uuid
        router_model_class : Interview
        relationship : APPARTIENT_A
        search_field : titre
        ordered_by : r.position
        """
        super().__init__(
            ExtraitSerializer,
            Extrait,
            "interview_uuid",
            Interview,
            "APPARTIENT_A",
            "titre",
            "r.position",
            **kwargs
        )

    def get_context_model(self) -> StructuredNode:
        """
        Récupère le node router,
        pour la gestion de la position des extraits dans le contexte d'une interview
        """
        try:
            router_nodeset: NodeSet = self.router_model_class.nodes
            return router_nodeset.get(uuid=self.kwargs[self.router_lookup_field])
        # N'est jamais sensé passer pas ici, raise déjà dans get_nodeset
        except DoesNotExist:  # pragma: no cover
            raise NotFound(self.router_model_class)  # pragma: no cover
        # Dans le cas ou la base de données était inaccessible
        except ServiceUnavailable:  # pragma: no cover
            raise ConnexionDB()  # pragma: no cover

    def get_serializer_context(self):
        """
        Modification du contexte du sérializer,
        pour la gestion de la position des extraits dans le contexte d'une interview
        """
        context = super().get_serializer_context()
        context_model_name: str = self.router_model_class.__name__
        context[context_model_name.lower()] = self.get_context_model()
        return context


class AudioExtraitViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'un audio:
    - GET /audios/{audio_uuid}/extraits/ : Renvoie la liste de tous les extraits liés à l'audio avec l'uuid spécifié
    - GET /audios/{audio_uuid}/extraits/{uuid}/ : Renvoie les détails de l'extrait avec l'uuid spécifié lié à l'audio avec l'uuid spécifié
    - POST /audios/{audio_uuid}/extraits/ : Crée un nouvel extrait non lié à un audio par défaut, création d'un extrait classique
    - PUT /audios/{audio_uuid}/extraits/{uuid}/ : Met à jour l'extrait avec l'uuid spécifié lié à l'audio avec l'uuid spécifié
    - PATCH /audios/{audio_uuid}/extraits/{uuid}/ : Met à jour partiellement l'extrait avec l'uuid spécifié lié à l'audio avec l'uuid spécifié
    - DELETE /audios/{audio_uuid}/extraits/{uuid}/ : Supprime l'extrait avec l'uuid spécifié lié à l'audio avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Extrait en fonction d'un node Audio

        serializer : ExtraitSerializer
        node : Extrait
        router_lookup_field : audio_uuid
        router_model_class : Audio
        relationship : AUDIOS
        search_field : titre
        """
        super().__init__(
            ExtraitSerializer, Extrait, "audio_uuid", Audio, "AUDIOS", "titre", **kwargs
        )


class TagExtraitViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'un tag:
    - GET /tags/{tag_uuid}/extraits/ : Renvoie la liste de tous les extraits liés au tag avec l'uuid spécifié
    - GET /tags/{tag_uuid}/extraits/{uuid}/ : Renvoie les détails de l'extrait avec l'uuid spécifié lié au tag avec l'uuid spécifié
    - POST /tags/{tag_uuid}/extraits/ : Crée un nouvel extrait non lié à un tag par défaut, création d'un extrait classique
    - PUT /tags/{tag_uuid}/extraits/{uuid}/ : Met à jour l'extrait avec l'uuid spécifié lié au tag avec l'uuid spécifié
    - PATCH /tags/{tag_uuid}/extraits/{uuid}/ : Met à jour partiellement l'extrait avec l'uuid spécifié lié au tag avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Extrait en fonction d'un node Tag

        serializer : ExtraitSerializer
        node : Extrait
        router_lookup_field : tag_uuid
        router_model_class : Tag
        relationship : TAGS_EXTRAIT
        search_field : titre
        """
        super().__init__(
            ExtraitSerializer,
            Extrait,
            "tag_uuid",
            Tag,
            "TAGS_EXTRAIT",
            "titre",
            **kwargs
        )


class ArtisteExtraitViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'un artiste:
    - GET /artistes/{artiste_uuid}/extraits/ : Renvoie la liste de tous les extraits liés à l'artiste avec l'uuid spécifié
    - GET /artistes/{artiste_uuid}/extraits/{uuid}/ : Renvoie les détails de l'extrait avec l'uuid spécifié lié à l'artiste avec l'uuid spécifié
    - POST /artistes/{artiste_uuid}/extraits/ : Crée un nouvel extrait non lié à un artiste par défaut, création d'un extrait classique
    - PUT /artistes/{artiste_uuid}/extraits/{uuid}/ : Met à jour l'extrait avec l'uuid spécifié lié à l'artiste avec l'uuid spécifié
    - PATCH /artistes/{artiste_uuid}/extraits/{uuid}/ : Met à jour partiellement l'extrait avec l'uuid spécifié lié à l'artiste avec l'uuid spécifié
    - DELETE /artistes/{artiste_uuid}/extraits/{uuid}/ : Supprime l'extrait avec l'uuid spécifié lié à l'artiste avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        super().__init__(
            ExtraitSerializer,
            Extrait,
            "artiste_uuid",
            Artiste,
            "PARTICIPER",
            "titre",
            **kwargs
        )
