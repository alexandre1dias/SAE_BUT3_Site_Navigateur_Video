# Modèle Conceptuel de Données (MCD)

## Code Mocodo

À copier directement sur mocodo.net :

```text
GENRE_MUSICAL: id_genre, nom_genre, code_couleur
APPARTENIR, 0N ARTISTE, 0N GENRE_MUSICAL
ARTISTE: id_artiste, nom_artiste
DONNER, 11 INTERVIEW, 0N ARTISTE
LIEU: id_lieu, nom_lieu, ville, pays

ACCUEILLIR, 11 INTERVIEW, 0N LIEU
INTERVIEW: id_interview, titre_interview, date_tournage, description, url_youtube, url_vimeo
COMPOSER, 11 EXTRAIT, 1N INTERVIEW
:
:

UTILISATEUR: id_utilisateur, nom_utilisateur, email, mot_de_passe, lecteur_prefere, est_admin
:
EXTRAIT: id_extrait, titre_extrait, ordre_sequence, timecode_debut, timecode_fin, url_youtube, url_vimeo, transcription
ASSOCIER, 11 EXTRAIT, 0N QUESTION
QUESTION: id_question, texte_question
```

## Capture d'écran du diagramme MCD
![Capture d'écran du diagramme MCD](<media/capture diagramme MCD.png>)