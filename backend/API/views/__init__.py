"""
Module d'initialisation pour les vues de l'API

Classes:
- BaseModelViewSet : Vue de base pour les opérations CRUD sur les modèles
- SubBaseModelViewSet : Vue de base pour les opérations CRUD sur les sous-modèles
- BaseRelationShipViewSet : Vue de base pour les opérations CRUD sur les relations entre les modèles
- ThemeViewSet : Vue pour les thèmes
- QuestionViewSet : Vue pour les questions
- ThemeQuestionViewSet : Vue pour les questions liées à un thème
- ExtraitViewSet : Vue pour les extraits
- QuestionExtraitViewSet : Vue pour les extraits liés à une question
- InterviewViewSet : Vue pour les interviews
- ArtisteViewSet : Vue pour les artistes
- UtilisateurViewSet : Vue pour les utilisateurs
- TagViewSet : Vue pour les tags
- RecherchesArtistesViewSet : Vue pour les recherches d'artistes liées à un utilisateur
- RegarderInterviewsViewSet : Vue pour les interviews regardées liées à un utilisateur
- RegarderExtraitsViewSet : Vue pour les extraits regardés liées à un utilisateur
- RecherchesQuestionsViewSet : Vue pour les recherches de questions liées à un utilisateur
- InterviewsViewSet : Vue pour les interviews liées à un extrait
- TagsExtraitRelationShipViewSet : Vue pour les relations entre les extraits et les tags
- TagsInterviewRelationShipViewSet : Vue pour les relations entre les interviews et les tags
- AudioViewSet : Vue pour les audios
- AudiosViewSet : Vue pour les audios liés à un extrait
- AudioExtraitViewSet : Vue pour les audios liés à un extrait
- OccationInterviewViewSet : Vue pour les occasions liées à une interview
- OccasionViewSet : Vue pour les occasions
- Recommandation : Vue pour les recommandations d'extraits
- CSVImportView : Vue pour l'importation de données à partir d'un fichier CSV
"""

from .base import BaseModelViewSet, SubBaseModelViewSet, BaseRelationShipViewSet
from .theme import ThemeViewSet
from .question import QuestionViewSet, ThemeQuestionViewSet
from .extrait import (
    ExtraitViewSet,
    TagExtraitViewSet,
    ArtisteExtraitViewSet,
    QuestionExtraitViewSet,
    InterviewExtraitViewSet,
    AudioExtraitViewSet,
)
from .interview import InterviewViewSet, TagInterviewViewSet, OccationInterviewViewSet
from .artiste import ArtisteViewSet
from .utilisateur import UtilisateurViewSet
from .tag import TagViewSet
from .recherches_artistes import RecherchesArtistesViewSet
from .regarder_interviews import RegarderInterviewsViewSet
from .regarder_extraits import RegarderExtraitsViewSet
from .recherches_questions import RecherchesQuestionsViewSet
from .interviews import InterviewsViewSet
from .tags_extrait import TagsExtraitRelationShipViewSet
from .tags_interview import TagsInterviewRelationShipViewSet
from .audio import AudioViewSet
from .audios import AudiosViewSet
from .occasion import OccasionViewSet
from .recommandation import Recommandation
from .csv_import import CSVImportView


__all__ = (
    "BaseModelViewSet",
    "SubBaseModelViewSet",
    "BaseRelationShipViewSet",
    "ThemeViewSet",
    "QuestionViewSet",
    "ThemeQuestionViewSet",
    "ExtraitViewSet",
    "TagExtraitViewSet",
    "ArtisteExtraitViewSet",
    "QuestionExtraitViewSet",
    "InterviewExtraitViewSet",
    "InterviewViewSet",
    "TagInterviewViewSet",
    "ArtisteViewSet",
    "UtilisateurViewSet",
    "TagViewSet",
    "RecherchesArtistesViewSet",
    "RegarderInterviewsViewSet",
    "RegarderExtraitsViewSet",
    "RecherchesQuestionsViewSet",
    "InterviewsViewSet",
    "TagsExtraitRelationShipViewSet",
    "TagsInterviewRelationShipViewSet",
    "AudioViewSet",
    "AudiosViewSet",
    "AudioExtraitViewSet",
    "OccationInterviewViewSet",
    "OccasionViewSet",
    "Recommandation",
    "CSVImportView",
)
