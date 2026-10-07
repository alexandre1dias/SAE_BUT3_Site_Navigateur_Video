from django.urls import path, include, re_path
from django.views.generic import *
from django.contrib.auth import views as auth_views
from . import  views
from . import views_api

urlpatterns=[
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("", views.HomeView.as_view(), name="home"),
    path('artists',views.get_artists,name='artists'),
    path('get_graph_data', views.get_graph_data, name='map'),
    path('artist/<str:node_id>', views.artist_detail, name='artist_detail'),
    path('theme/<str:node_id>', views.theme_detail, name='theme_detail'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/search', views.api_search, name='search'),
    path('api/question/<str:question_id>/', views_api.get_similar_questions, name='question_api'),
    path('interview/chose/',views.chose_interview, name="chose_interview" ),
    path('video/<str:interview_id>/create/',views.create_video, name="create_video" ),
    path('video/<str:video_id>/', views.get_video, name='lecteur'),
    path('interview/<str:interview_id>/update/',views.update_interview, name="update_interview" ),
    path('video/<str:video_id>/update/',views.update_video, name="update_video" ),
    path('interview/<str:interview_id>/', views.watch_interview, name='interview'),
    path('add-question/', views.add_question, name='add_question'),
    path('add-artist/', views.add_artist, name='add_artist'),
    path('add-theme/', views.add_theme, name='add_theme'),
    path('add-style/', views.add_style, name='add_style'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-interview/', views.add_interview, name='add_interview'),
    re_path(r'^download-transcription/(?P<url>.+)/$', views.download_transcription, name="download_transcription"),
    path('clear_graph_cache/', views.clear_graph_cache, name='clear_graph_cache'),
]