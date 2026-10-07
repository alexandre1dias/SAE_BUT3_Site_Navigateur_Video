"""
Liste des urls et routers de l'API
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import *
from .views.csv_import_job_status import CSVImportJobStatusView

router = DefaultRouter()


router.register(r"themes", ThemeViewSet, basename="theme")
router_theme = NestedDefaultRouter(router, r"themes", lookup="theme")
router_theme.register(r"questions", ThemeQuestionViewSet, basename="question")


router.register(r"questions", QuestionViewSet, basename="question")
router_question = NestedDefaultRouter(router, r"questions", lookup="question")
router_question.register(r"extraits", QuestionExtraitViewSet, basename="extrait")


router.register(r"extraits", ExtraitViewSet, basename="extrait")
router_extrait = NestedDefaultRouter(router, r"extraits", lookup="extrait")
router_extrait.register(r"interviews", InterviewsViewSet, basename="interview")
router_extrait.register(r"audios", AudiosViewSet, basename="audio")
router_extrait.register(r"tags", TagsExtraitRelationShipViewSet, basename="tag")


router.register(r"interviews", InterviewViewSet, basename="interview")
router_interview = NestedDefaultRouter(router, r"interviews", lookup="interview")
router_interview.register(r"extraits", InterviewExtraitViewSet, basename="extrait")
router_interview.register(r"tags", TagsInterviewRelationShipViewSet, basename="tag")


router.register(r"artistes", ArtisteViewSet, basename="artiste")
router_artiste = NestedDefaultRouter(router, r"artistes", lookup="artiste")
router_artiste.register(r"extraits", ArtisteExtraitViewSet, basename="extrait")

router.register(r"occasions", OccasionViewSet, basename="occasion")
router_occasion = NestedDefaultRouter(router, r"occasions", lookup="occasion")
router_occasion.register(r"interviews", OccationInterviewViewSet, basename="interview")

router.register(r"audios", AudioViewSet, basename="audio")
router_audio = NestedDefaultRouter(router, r"audios", lookup="audio")
router_audio.register(r"extraits", AudioExtraitViewSet, basename="extrait")


router.register(r"tags", TagViewSet, basename="tag")
router_tag = NestedDefaultRouter(router, r"tags", lookup="tag")
router_tag.register(r"extraits", TagExtraitViewSet, basename="extrait")
router_tag.register(r"interviews", TagInterviewViewSet, basename="interview")


router.register(r"utilisateurs", UtilisateurViewSet, basename="utilisateur")
router_utilisateur = NestedDefaultRouter(router, r"utilisateurs", lookup="utilisateur")
router_utilisateur.register(r"artistes", RecherchesArtistesViewSet, basename="artiste")
router_utilisateur.register(
    r"interviews", RegarderInterviewsViewSet, basename="interview"
)
router_utilisateur.register(r"extraits", RegarderExtraitsViewSet, basename="extrait")
router_utilisateur.register(
    r"questions", RecherchesQuestionsViewSet, basename="question"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router_theme.urls)),
    path("", include(router_question.urls)),
    path("", include(router_extrait.urls)),
    path("", include(router_interview.urls)),
    path("", include(router_artiste.urls)),
    path("", include(router_audio.urls)),
    path("", include(router_tag.urls)),
    path("", include(router_utilisateur.urls)),
    path("", include(router_occasion.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),
    path("login/verify/", TokenVerifyView.as_view(), name="login-verify"),
    path("recommandations", Recommandation.as_view(), name="recommandation"),
    path("csv_import/", CSVImportView.as_view(), name="csv_import"),
    path('csv_import/status/<str:job_uuid>/', CSVImportJobStatusView.as_view(), name='csv_import_status'),
]
