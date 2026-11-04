from django.contrib import admin

from .models import Artiste, Extrait, GenreMusical, Interview, Lieu, ProfilUtilisateur, Question

# Les vidéos se gèrent surtout depuis la page « Administration » du site (/rec117/administration/).
# L'administration Django (/admin/) sert pour le reste : artistes, genres, lieux, questions, comptes.
for modele in (GenreMusical, Artiste, Lieu, Question, Interview, Extrait, ProfilUtilisateur):
    admin.site.register(modele)
