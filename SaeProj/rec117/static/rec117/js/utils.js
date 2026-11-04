// === Fonctions d'affichage communes aux pages ===
// À charger après data.js

function creerElement(balise, classe, texte) {
    const element = document.createElement(balise);
    if (classe) element.className = classe;
    if (texte) element.textContent = texte;
    return element;
}

// Pastille à la couleur du genre (colonne codeCouleur)
function creerPastille(genre) {
    const pastille = creerElement('span', 'color-badge');
    pastille.style.setProperty('--couleur-genre', genre.codeCouleur);
    return pastille;
}

function nomsDesGenres(genres) {
    return genres.map(genre => genre.nomGenre).join(', ');
}

function texteLieu(lieu) {
    return lieu ? `${lieu.nomLieu}, ${lieu.villeLieu}` : 'Lieu non précisé';
}

// Convertit une durée ou un timecode en secondes vers le format mm:ss
function formaterTimecode(secondes) {
    const minutes = Math.floor(secondes / 60);
    return `${String(minutes).padStart(2, '0')}:${String(secondes % 60).padStart(2, '0')}`;
}

// Accepte une date ('2026-03-14') ou un horodatage SQL ('2026-03-14 18:30:00')
function formaterDate(dateSql) {
    return new Date(dateSql.replace(' ', 'T')).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
}

// La base ne stocke pas de miniature : la maquette utilise des images d'illustration
function imageInterview(interview, largeur, hauteur) {
    return `https://picsum.photos/${largeur}/${hauteur}?random=${30 + interview.idInterview}`;
}

function imageExtrait(extrait, largeur, hauteur) {
    return `https://picsum.photos/${largeur}/${hauteur}?random=${200 + extrait.idExtrait}`;
}
