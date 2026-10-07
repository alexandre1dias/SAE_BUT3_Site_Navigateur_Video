"""
Module contenant tous les sérializers de l'API

Classes :
    - ArtisteSerializer : sérializer du node Artiste
    - AudioSerializer : sérializer du node Audio
    - ExtraitSerializer : sérializer du node Extrait
    - InterviewSerializer : sérializer du node Interview
    - OccasionSerializer : sérializer du node Occasion
    - QuestionSerializer : sérializer du node Question
    - TagSerializer : sérializer du node Tag
    - ThemeSerializer : sérializer du node Theme
    - UtilisateurSerializer : sérializer du node Utilisateur
    - RecherchesArtistesSerializer : sérializer du node RecherchesArtistes
    - RecherchesQuestionsSerializer : sérializer du node RecherchesQuestions
    - RegarderInterviewsSerializer : sérializer du node RegarderInterviews
    - RegarderExtraitsSerializer : sérializer du node RegarderExtraits
    - TagsExtraitRelationShipSerializer : sérializer de la relation tags_extrait (Extrait <-> Tag)
    - TagsInterviewRelationShipSerializer : sérializer de la relation tags_interview (Interview <-> Tag)
    - AudiosSerializer : sérializer de la relation audios (Extrait <-> Audio)
    - InterviewsSerializer : sérializer de la relation interviews (Extrait <-> Interview)
    - PositionInputSerializer : sérializer pour la mise à jour de la position d'un extrait dans une interview
    - TokenObtain : sérializer pour l'obtention d'un token JWT
    - TokenRefresh : sérializer pour le rafraîchissement d'un token JWT
"""

from .base import *
from .theme import ThemeSerializer
from .question import QuestionSerializer
from .extrait import ExtraitSerializer
from .interview import InterviewSerializer
from .artiste import ArtisteSerializer
from .utilisateur import UtilisateurSerializer
from .tag import TagSerializer
from .recherches_artistes import RecherchesArtistesSerializer
from .regarder_interviews import RegarderInterviewsSerializer
from .regarder_extraits import RegarderExtraitsSerializer
from .recherches_questions import RecherchesQuestionsSerializer
from .interviews import InterviewsSerializer, PositionInputSerializer
from .tags_extrait import TagsExtraitRelationShipSerializer
from .tags_interview import TagsInterviewRelationShipSerializer
from .audio import AudioSerializer
from .audios import AudiosSerializer
from .occasion import OccasionSerializer
from .auth import *

__all__ = (
    "BaseSerializer",
    "BaseRelationShipSerializer",
    "RelationShipUtilisateurSerializer",
    "RelationShipTagSerializer",
    "ThemeSerializer",
    "QuestionSerializer",
    "ExtraitSerializer",
    "InterviewSerializer",
    "ArtisteSerializer",
    "UtilisateurSerializer",
    "TagSerializer",
    "RecherchesArtistesSerializer",
    "RegarderInterviewsSerializer",
    "RegarderExtraitsSerializer",
    "RecherchesQuestionsSerializer",
    "InterviewsSerializer",
    "PositionInputSerializer",
    "TagsExtraitRelationShipSerializer",
    "TagsInterviewRelationShipSerializer",
    "AudioSerializer",
    "AudiosSerializer",
    "OccasionSerializer",
    "TokenObtain",
    "TokenRefresh",
)
