from rest_framework import status
from rest_framework.response import Response
from ..models import Interview, Extrait, PositionExtraitRel
from ..serializers import InterviewsSerializer, PositionInputSerializer
from . import BaseRelationShipViewSet


class InterviewsViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les interviews liées à un extrait, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les interviews liées à un extrait:
    - GET /extraits/{extrait_uuid}/interviews/ : Renvoie la liste de tous les interviews liés à l'extrait avec l'uuid spécifié
    - GET /extraits/{extrait_uuid}/interviews/{interview_uuid}/ : Renvoie les détails de l'interview avec l'uuid spécifié lié à l'extrait avec l'uuid spécifié
    - POST /extraits/{extrait_uuid}/interviews/ : Crée une nouvelle relation APPARTIENT_A entre interview et extrait avec l'uuid spécifié
    - PATCH /extraits/{extrait_uuid}/interviews/{interview_uuid}/ : Modifie la position de l'interview avec l'uuid spécifié lié à l'extrait avec l'uuid spécifié
    - DELETE /extraits/{extrait_uuid}/interviews/{interview_uuid}/ : Supprime la relation APPARTIENT_A entre l'interview avec l'uuid spécifié et l'extrait avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Interview lié à Extrait

        serializer : InterviewsSerializer
        node : Interview
        router_lookup_field : extrait_uuid
        router_model_class : Extrait
        relationship : APPARTIENT_A
        search_field : titre
        """
        super().__init__(
            InterviewsSerializer,
            Interview,
            "extrait_uuid",
            Extrait,
            "APPARTIENT_A",
            "titre",
            **kwargs
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Permet de modifier la position d'une interview liée à un extrait

        position : Nouvelle position de l'interview dans l'extrait (entier positif)
        """
        serializer_in = PositionInputSerializer(data=request.data)
        serializer_in.is_valid(raise_exception=True)
        new_position = serializer_in.validated_data["position"]

        interview: Interview = self.get_object()
        extrait: Extrait = self.get_context_model()
        rel: PositionExtraitRel = extrait.interviews.relationship(interview)
        rel.position = int(new_position)
        rel.save()
        return Response(
            self.get_serializer(interview, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )
