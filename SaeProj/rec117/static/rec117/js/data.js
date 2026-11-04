// === Données du site ===
// Envoyées par la vue (views.py, donnees_pour_js) et écrites dans la page par
// {{ donnees|json_script:"donnees" }}. Une constante par table, avec les noms des champs des modèles Django.
const { GENRE_MUSICAL, ARTISTE, ARTISTE_GENRE, LIEU, QUESTION, INTERVIEW, EXTRAIT } =
    JSON.parse(document.getElementById('donnees').textContent);

// === Fonctions d'accès aux données ===
// Elles jouent le rôle des jointures SQL entre les tables.

function trouver(table, colonne, valeur) {
    return table.find(ligne => ligne[colonne] === valeur);
}

function artisteDeInterview(interview) {
    return trouver(ARTISTE, 'idArtiste', interview.artiste_id);
}

function lieuDeInterview(interview) {
    return trouver(LIEU, 'idLieu', interview.lieu_id) || null;
}

function genresDeArtiste(artiste) {
    return ARTISTE_GENRE
        .filter(lien => lien.artiste_id === artiste.idArtiste)
        .map(lien => trouver(GENRE_MUSICAL, 'idGenre', lien.genremusical_id));
}

// Extraits d'une interview, dans l'ordre de la séquence
function extraitsDeInterview(interview) {
    return EXTRAIT
        .filter(extrait => extrait.interview_id === interview.idInterview)
        .sort((a, b) => a.ordreSequence - b.ordreSequence);
}

function interviewDeExtrait(extrait) {
    return trouver(INTERVIEW, 'idInterview', extrait.interview_id);
}

function questionDeExtrait(extrait) {
    return trouver(QUESTION, 'idQuestion', extrait.question_id);
}
