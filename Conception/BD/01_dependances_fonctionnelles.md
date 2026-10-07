# Dépendances Fonctionnelles (DF)

### Entités principales :
* `id_genre` -> `nom_genre`, `code_couleur`
* `id_artiste` -> `nom_artiste`, `biographie`, `photo_url`
* `id_lieu` -> `nom_lieu`, `ville`, `pays`
* `id_theme` -> `titre_theme`, `description_theme`
* `id_question` -> `texte_question`, `description_question`, `id_theme`
* `id_interview` -> `titre_interview`, `date_tournage`, `description`, `url_youtube`, `url_vimeo`, `id_artiste`, `id_lieu`
* `id_extrait` -> `titre_extrait`, `ordre_sequence`, `timecode_debut`, `timecode_fin`, `url_youtube`, `url_vimeo`, `transcription`, `id_interview`, `id_question`
* `id_utilisateur` -> `nom_utilisateur`, `email`, `mot_de_passe`, `lecteur_prefere`
* `id_playlist` -> `titre_playlist`, `date_creation`, `id_utilisateur`

### Dépendances fonctionnelles composées / associations :
* `(id_artiste, id_genre)` (association n:m)
* `(id_interview, ordre_sequence)` -> `id_extrait`
* `(id_playlist, id_extrait)` -> `position`
* `(id_playlist, position)` -> `id_extrait`