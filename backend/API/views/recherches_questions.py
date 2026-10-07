from ..models import Question, Utilisateur
from ..serializers import RecherchesQuestionsSerializer
from ..permissions import IsUserOrAdmin
from . import BaseRelationShipViewSet


class RecherchesQuestionsViewSet(BaseRelationShipViewSet):
    """
    ViewSet pour les recherches de questions liées à un utilisateur, héritant de BaseRelationShipViewSet

    CRUD incomplet pour les recherches de questions liées à un utilisateur:
    - GET /utilisateurs/{utilisateur_uuid}/recherches_questions/ : Renvoie la liste de tous les questions recherchés liés à l'utilisateur avec l'uuid spécifié
    - GET /utilisateurs/{utilisateur_uuid}/recherches_questions/{question_uuid}/ : Renvoie les détails de la question recherchée avec l'uuid spécifié lié à l'utilisateur avec l'uuid spécifié
    - POST /utilisateurs/{utilisateur_uuid}/recherches_questions/ : Crée une nouvelle relation RECHERCHES_QUESTIONS entre question et utilisateur avec l'uuid spécifié
    - DELETE /utilisateurs/{utilisateur_uuid}/recherches_questions/{question_uuid}/ : Supprime la relation RECHERCHES_QUESTIONS entre la question avec l'uuid spécifié et l'utilisateur avec l'uuid spécifié

    permission_classes : IsUserOrAdmin (Seuls les utilisateurs eux-mêmes ou les administrateurs peuvent accéder à ces actions)
    """

    permission_classes = [IsUserOrAdmin]

    def __init__(self, **kwargs):
        """
        RelationShip ViewSet du node Question lié à Utilisateur

        serializer : RecherchesQuestionsSerializer
        node : Question
        router_lookup_field : utilisateur_uuid
        router_model_class : Utilisateur
        relationship : RECHERCHES_QUESTIONS
        search_field : texte
        """
        super().__init__(
            RecherchesQuestionsSerializer,
            Question,
            "utilisateur_uuid",
            Utilisateur,
            "RECHERCHES_QUESTIONS",
            "texte",
            **kwargs
        )
