### `Conception/BD/03_mld.md`

```markdown
# Modèle Logique de Données (MLD)

* **GENRE_MUSICAL** (<u>id_genre</u>, nom_genre, code_couleur)
* **ARTISTE** (<u>id_artiste</u>, nom_artiste, biographie, photo_url)
* **ARTISTE_GENRE** (<u>#id_artiste, #id_genre</u>)
* **LIEU** (<u>id_lieu</u>, nom_lieu, ville, pays)
* **THEME** (<u>id_theme</u>, titre_theme, description_theme)
* **QUESTION** (<u>id_question</u>, texte_question, description_question, #id_theme)
* **INTERVIEW** (<u>id_interview</u>, titre_interview, date_tournage, description, url_youtube, url_vimeo, #id_artiste, #id_lieu)
* **EXTRAIT** (<u>id_extrait</u>, titre_extrait, ordre_sequence, timecode_debut, timecode_fin, url_youtube, url_vimeo, transcription, #id_interview, #id_question)
* **UTILISATEUR** (<u>id_utilisateur</u>, nom_utilisateur, email, mot_de_passe, lecteur_prefere)
* **PLAYLIST** (<u>id_playlist</u>, titre_playlist, date_creation, #id_utilisateur)
* **PLAYLIST_EXTRAIT** (<u>#id_playlist, #id_extrait</u>, position)

### Notes :
* Les clés primaires sont soulignées (`<u>...</u>`).
* Les clés étrangères commencent par `#`.
* Contrainte d'unicité sur `EXTRAIT` : le couple `(#id_interview, ordre_sequence)` doit être unique.
* Contrainte d'unicité sur `PLAYLIST_EXTRAIT` : le couple `(#id_playlist, position)` doit être unique.