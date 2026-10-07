from ..models import Interview, Occasion, Tag
from ..serializers import InterviewSerializer
from . import BaseModelViewSet, SubBaseModelViewSet


class InterviewViewSet(BaseModelViewSet):
    """
    ViewSet pour les interviews, héritant de BaseModelViewSet

    CRUD complet pour les interviews:
    - GET /interviews/ : Renvoie la liste de tous les interviews
    - GET /interviews/{uuid}/ : Renvoie les détails de l'interview avec l'uuid spécifié
    - POST /interviews/ : Crée un nouvel interview
    - PUT /interviews/{uuid}/ : Met à jour l'interview avec l'uuid spécifié
    - PATCH /interviews/{uuid}/ : Met à jour partiellement l'interview avec l'uuid spécifié
    - DELETE /interviews/{uuid}/ : Supprime l'interview avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Interview

        serializer : InterviewSerializer
        node : Interview
        search_field : titre
        """
        super().__init__(InterviewSerializer, Interview, "titre", **kwargs)


class TagInterviewViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'un tag:
    - GET /tags/{tag_uuid}/interviews/ : Renvoie la liste de tous les interviews liés au tag avec l'uuid spécifié
    - GET /tags/{tag_uuid}/interviews/{uuid}/ : Renvoie les détails de l'interview avec l'uuid spécifié lié au tag avec l'uuid spécifié
    - POST /tags/{tag_uuid}/interviews/ : Crée un nouvel interview non lié à un tag par défaut, création d'un interview classique
    - PUT /tags/{tag_uuid}/interviews/{uuid}/ : Met à jour l'interview avec l'uuid spécifié lié au tag avec l'uuid spécifié
    - PATCH /tags/{tag_uuid}/interviews/{uuid}/ : Met à jour partiellement l'interview avec l'uuid spécifié lié au tag avec l'uuid spécifié
    - DELETE /tags/{tag_uuid}/interviews/{uuid}/ : Supprime l'interview avec l'uuid spécifié lié au tag avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Interview en fonction d'un node Tag

        serializer : InterviewSerializer
        node : Interview
        router_lookup_field : tag_uuid
        router_model_class : Tag
        relationship : TAGS_INTERVIEW
        search_field : titre
        """
        super().__init__(
            InterviewSerializer,
            Interview,
            "tag_uuid",
            Tag,
            "TAGS_INTERVIEW",
            "titre",
            **kwargs
        )


class OccationInterviewViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les extraits, héritant de SubBaseModelViewSet

    CRUD complet pour les extraits en fonction d'une occasion:
    - GET /occasions/{occasion_uuid}/interviews/ : Renvoie la liste de tous les interviews liés à l'occasion avec l'uuid spécifié
    - GET /occasions/{occasion_uuid}/interviews/{uuid}/ : Renvoie les détails de l'interview avec l'uuid spécifié lié à l'occasion avec l'uuid spécifié
    - POST /occasions/{occasion_uuid}/interviews/ : Crée un nouvel interview non lié à une occasion par défaut, création d'un interview classique
    - PUT /occasions/{occasion_uuid}/interviews/{uuid}/ : Met à jour l'interview avec l'uuid spécifié lié à l'occasion avec l'uuid spécifié
    - PATCH /occasions/{occasion_uuid}/interviews/{uuid}/ : Met à jour partiellement l'interview avec l'uuid spécifié lié à l'occasion avec l'uuid spécifié
    - DELETE /occasions/{occasion_uuid}/interviews/{uuid}/ : Supprime l'interview avec l'uuid spécifié lié à l'occasion avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Interview en fonction d'un node Occasion

        serializer : InterviewSerializer
        node : Interview
        router_lookup_field : occasion_uuid
        router_model_class : Occasion
        relationship : OCCASION
        search_field : titre
        """
        super().__init__(
            InterviewSerializer,
            Interview,
            "occasion_uuid",
            Occasion,
            "OCCASION",
            "titre",
            **kwargs
        )
