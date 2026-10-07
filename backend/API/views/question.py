from ..models import Question, Theme
from ..serializers import QuestionSerializer
from . import BaseModelViewSet, SubBaseModelViewSet


class QuestionViewSet(BaseModelViewSet):
    """
    ViewSet pour les questions, héritant de BaseModelViewSet

    CRUD complet pour les questions:
    - GET /questions/ : Renvoie la liste de tous les questions
    - GET /questions/{uuid}/ : Renvoie les détails de la question avec l'uuid spécifié
    - POST /questions/ : Crée un nouvel question
    - PUT /questions/{uuid}/ : Met à jour la question avec l'uuid spécifié
    - PATCH /questions/{uuid}/ : Met à jour partiellement la question avec l'uuid spécifié
    - DELETE /questions/{uuid}/ : Supprime la question avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Question

        serializer : QuestionSerializer
        node : Question
        search_field : texte
        """
        super().__init__(QuestionSerializer, Question, "texte", **kwargs)


class ThemeQuestionViewSet(SubBaseModelViewSet):
    """
    ViewSet pour les questions, héritant de SubBaseModelViewSet

    CRUD complet pour les questions en fonction d'un thème:
    - GET /themes/{theme_uuid}/questions/ : Renvoie la liste de tous les questions liés au thème avec l'uuid spécifié
    - GET /themes/{theme_uuid}/questions/{uuid}/ : Renvoie les détails de la question avec l'uuid spécifié lié au thème avec l'uuid spécifié
    - POST /themes/{theme_uuid}/questions/ : Crée un nouvel question non lié à un thème par défaut, création d'un question classique
    - PUT /themes/{theme_uuid}/questions/{uuid}/ : Met à jour la question avec l'uuid spécifié lié au thème avec l'uuid spécifié
    - PATCH /themes/{theme_uuid}/questions/{uuid}/ : Met à jour partiellement la question avec l'uuid spécifié lié au thème avec l'uuid spécifié
    - DELETE /themes/{theme_uuid}/questions/{uuid}/ : Supprime la question avec l'uuid spécifié lié au thème avec l'uuid spécifié
    """

    def __init__(self, **kwargs):
        """
        ModelViewSet du node Question en fonction d'un node Theme

        serializer : QuestionSerializer
        node : Question
        router_lookup_field : theme_uuid
        router_model_class : Theme
        relationship : A_THEME
        search_field : texte
        """
        super().__init__(
            QuestionSerializer,
            Question,
            "theme_uuid",
            Theme,
            "A_THEME",
            "texte",
            **kwargs
        )
