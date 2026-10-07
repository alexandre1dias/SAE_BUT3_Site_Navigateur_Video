# Modèle Conceptuel de Données (MCD)

## Code Mocodo

À copier directement sur mocodo.net :

```text
GENRE_MUSICAL: id_genre, nom_genre, code_couleur
APPARTENIR, 0N ARTISTE, 0N GENRE_MUSICAL
ARTISTE: id_artiste, nom_artiste, biographie, photo_url
DONNER, 11 INTERVIEW, 0N ARTISTE
LIEU: id_lieu, nom_lieu, ville, pays

ACCUEILLIR, 11 INTERVIEW, 0N LIEU
INTERVIEW: id_interview, titre_interview, date_tournage, description, url_youtube, url_vimeo
COMPOSER, 11 EXTRAIT, 1N INTERVIEW
THEME: id_theme, titre_theme, description_theme
REGROUPER, 11 QUESTION, 0N THEME

UTILISATEUR: id_utilisateur, nom_utilisateur, email, mot_de_passe, lecteur_prefere
CREER, 11 PLAYLIST, 0N UTILISATEUR
EXTRAIT: id_extrait, titre_extrait, ordre_sequence, timecode_debut, timecode_fin, url_youtube, url_vimeo, transcription
ASSOCIER, 11 EXTRAIT, 0N QUESTION
QUESTION: id_question, texte_question, description_question

PLAYLIST: id_playlist, titre_playlist, date_creation
CONTENIR, 0N EXTRAIT, 0N PLAYLIST: position
