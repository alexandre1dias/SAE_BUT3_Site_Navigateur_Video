# Modèle Logique de Données (MLD)

* **GENRE_MUSICAL** (<u>id_genre</u>, nom_genre, code_couleur)
* **ARTISTE** (<u>id_artiste</u>, nom_artiste)
* **ARTISTE_GENRE** (<u>#id_artiste, #id_genre</u>)
* **LIEU** (<u>id_lieu</u>, nom_lieu, ville, pays)
* **QUESTION** (<u>id_question</u>, texte_question)
* **INTERVIEW** (<u>id_interview</u>, titre_interview, date_tournage, description, url_youtube, url_vimeo, #id_artiste, #id_lieu)
* **EXTRAIT** (<u>id_extrait</u>, titre_extrait, ordre_sequence, timecode_debut, timecode_fin, url_youtube, url_vimeo, transcription, #id_interview, #id_question)
* **UTILISATEUR** (<u>id_utilisateur</u>, nom_utilisateur, email, mot_de_passe, lecteur_prefere, est_admin)

### Notes :
* Les clés étrangères commencent par `#`.
* Contrainte d'unicité sur `EXTRAIT` : `(#id_interview, ordre_sequence)` est unique pour respecter l'ordre dans la vidéo.