// === Page d'accueil (Mode Lecture) ===
// Les cartes et les menus sont déjà écrits par Django ; ce fichier gère le défilement et les filtres.

// La navbar devient opaque quand on descend
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 50));

// === Filtres ===
// Chaque carte porte data-artiste, data-lieu et data-genres (voir partials/carte.html).
// On cache les cartes qui ne correspondent pas aux trois menus.
const filtreGenre = document.getElementById('filter-genre');
const filtreLieu = document.getElementById('filter-lieu');
const filtreArtiste = document.getElementById('filter-artiste');
const cartes = document.querySelectorAll('.card');
const rechercheMotsCles = document.getElementById('search-keywords');
const rechercheDateDebut = document.getElementById('search-date-from');
const rechercheDateFin = document.getElementById('search-date-to');

function normaliserRecherche(texte) {
    return texte
        .toLocaleLowerCase('fr-FR')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
}

function filtrerVideos() {
    const motsCles = (rechercheMotsCles?.value || '')
        .trim()
        .toLocaleLowerCase('fr-FR')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .split(/\s+/)
        .filter(Boolean);
    const dateDebut = rechercheDateDebut?.value || '';
    const dateFin = rechercheDateFin?.value || '';

    cartes.forEach(carte => {
        const contenu = normaliserRecherche(carte.dataset.search || '');
        const date = carte.dataset.date || '';
        const correspond =
            (filtreGenre.value === '' || carte.dataset.genres.split(',').includes(filtreGenre.value)) &&
            (filtreLieu.value === '' || carte.dataset.lieu === filtreLieu.value) &&
            (filtreArtiste.value === '' || carte.dataset.artiste === filtreArtiste.value) &&
            motsCles.every(mot => contenu.includes(mot)) &&
            (!dateDebut || (date && date >= dateDebut)) &&
            (!dateFin || (date && date <= dateFin));

        carte.hidden = !correspond;
    });
}

[filtreGenre, filtreLieu, filtreArtiste].forEach(filtre => filtre.addEventListener('change', filtrerVideos));
[rechercheMotsCles, rechercheDateDebut, rechercheDateFin]
    .filter(Boolean)
    .forEach(filtre => filtre.addEventListener('input', filtrerVideos));

document.getElementById('search-reset')?.addEventListener('click', () => {
    rechercheMotsCles.value = '';
    rechercheDateDebut.value = '';
    rechercheDateFin.value = '';
    filtreGenre.value = '';
    filtreLieu.value = '';
    filtreArtiste.value = '';
    document.querySelectorAll('.chip-btn').forEach(bouton => {
        bouton.classList.toggle('active', bouton.dataset.value === '');
    });
    filtrerVideos();
});
