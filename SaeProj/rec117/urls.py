from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views, views_admin

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("home/", views.HomeView.as_view(), name="home_base"),  
    path("mindmap/", views.MindMapView.as_view(), name="mind_map"),
    path("connexion/", views.ConnexionUtilisateurView.as_view(), name="connexion"),
    path("deconnexion/", LogoutView.as_view(next_page="home"), name="deconnexion"),
    path("inscription/", views.inscription, name="inscription"),

    # Administration des vidéos (réservée aux comptes staff)
    path("administration/", views_admin.accueil, name="admin_videos"),
    path("administration/connexion/", views_admin.ConnexionView.as_view(), name="admin_connexion"),
    path("administration/deconnexion/", LogoutView.as_view(next_page="home"), name="admin_deconnexion"),
    path("administration/<str:type_video>/ajouter/", views_admin.ajouter, name="admin_ajouter"),
    path("administration/<str:type_video>/<int:pk>/modifier/", views_admin.modifier, name="admin_modifier"),
    path("administration/<str:type_video>/<int:pk>/supprimer/", views_admin.supprimer, name="admin_supprimer"),
]
