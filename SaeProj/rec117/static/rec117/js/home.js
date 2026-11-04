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

function filtrerVideos() {
    cartes.forEach(carte => {
        const correspond =
            (filtreGenre.value === '' || carte.dataset.genres.split(',').includes(filtreGenre.value)) &&
            (filtreLieu.value === '' || carte.dataset.lieu === filtreLieu.value) &&
            (filtreArtiste.value === '' || carte.dataset.artiste === filtreArtiste.value);

        carte.hidden = !correspond;
    });
}

[filtreGenre, filtreLieu, filtreArtiste].forEach(filtre => filtre.addEventListener('change', filtrerVideos));
