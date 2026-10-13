// === Page d'accueil (Mode Lecture) ===
// Les données (VIDEOS, ARTISTES, GENRES, LIEUX, VIDEO_A_LA_UNE) viennent de data.js

const videoParId = {};
VIDEOS.forEach(video => { videoParId[video.id] = video; });

const artisteParId = {};
ARTISTES.forEach(artiste => { artisteParId[artiste.id] = artiste; });

function genreDe(video) {
    return artisteParId[video.artiste].genre;
}

function urlImage(numero, largeur, hauteur) {
    return `https://picsum.photos/${largeur}/${hauteur}?random=${numero}`;
}

function creerElement(balise, classe, texte) {
    const element = document.createElement(balise);
    if (classe) element.className = classe;
    if (texte) element.textContent = texte;
    return element;
}

// === Gestion du défilement (Navbar) ===
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 50));

// === Cartes des vidéos ===
function creerCarte(video) {
    const carte = creerElement('div', 'card');
    carte.id = video.id;
    carte.dataset.genre = genreDe(video);
    carte.dataset.lieu = video.lieu;
    carte.dataset.artiste = video.artiste;

    const miniature = creerElement('img');
    miniature.src = urlImage(video.image, 400, 225);
    miniature.alt = 'Miniature';

    const etiquettes = creerElement('span', 'card-tags');
    etiquettes.append(
        creerElement('span', `color-badge genre-${genreDe(video)}`),
        ` ${video.duree || 'Question'} • ${LIEUX[video.lieu]}`
    );

    const infos = creerElement('div', 'card-info');
    infos.append(creerElement('span', 'card-title', video.titre), etiquettes);

    carte.append(miniature, infos);
    carte.addEventListener('click', () => ouvrirModal(video));
    return carte;
}

const carrouselQuestions = document.getElementById('questions-carousel');
const carrouselInterviews = document.getElementById('interviews-carousel');

VIDEOS.forEach(video => {
    const carrousel = video.format === 'interview' ? carrouselInterviews : carrouselQuestions;
    carrousel.appendChild(creerCarte(video));
});

// === Logique de la fenêtre Modale ===
const modal = document.getElementById('video-modal');

function ouvrirModal(video) {
    const genre = genreDe(video);
    const estInterview = video.format === 'interview';

    document.getElementById('modal-title').textContent = video.titre;
    document.getElementById('modal-desc').textContent = video.description;
    document.getElementById('modal-bg').style.backgroundImage =
        `url('${video.imageModale || urlImage(video.image, 800, 450)}')`;

    document.getElementById('modal-location').textContent = `📍 ${video.lieuTexte || LIEUX[video.lieu]}`;
    document.getElementById('modal-color-badge').className = `color-badge genre-${genre}`;
    document.getElementById('modal-genre-text').textContent = GENRES[genre].nomComplet;

    const badge = document.getElementById('modal-format-badge');
    badge.textContent = estInterview ? 'Interview Intégrale' : 'Extrait (Question)';
    badge.className = `format-badge ${video.format}`;
    document.getElementById('modal-meta-type').textContent =
        estInterview ? 'Interview Intégrale' : 'Extrait / Réponse spécifique';

    // Un bouton par bifurcation possible depuis cette vidéo
    const conteneurLiens = document.getElementById('modal-related-links');
    conteneurLiens.replaceChildren();

    video.liens.forEach(lien => {
        const cible = videoParId[lien.cible];
        if (!cible) return;

        const bouton = creerElement('button', 'btn-related', lien.texte);
        bouton.addEventListener('click', () => {
            ouvrirModal(cible);
            document.querySelector('.modal-content').scrollTop = 0; // Remonte la modale tout en haut
        });
        conteneurLiens.appendChild(bouton);
    });

    modal.classList.add('active');
    document.body.classList.add('modal-ouverte');
}

function fermerModal() {
    modal.classList.remove('active');
    document.body.classList.remove('modal-ouverte');
}

function lancerVideo() {
    const lecteur = document.getElementById('player-source').value;
    alert(`Lancement du lecteur vidéo via l'API : ${lecteur.toUpperCase()}`);
}

document.getElementById('hero-play').addEventListener('click', () => ouvrirModal(VIDEO_A_LA_UNE));
document.getElementById('modal-close').addEventListener('click', fermerModal);
document.getElementById('modal-play').addEventListener('click', lancerVideo);

// Un clic sur le fond sombre ferme la modale
modal.addEventListener('click', e => {
    if (e.target === modal) fermerModal();
});

// === Logique des filtres croisés de la base de données ===
const filtreGenre = document.getElementById('filter-genre');
const filtreLieu = document.getElementById('filter-lieu');
const filtreArtiste = document.getElementById('filter-artiste');
const cartes = document.querySelectorAll('.card');

function filtrerVideos() {
    cartes.forEach(carte => {
        const correspond =
            (filtreGenre.value === '' || carte.dataset.genre === filtreGenre.value) &&
            (filtreLieu.value === '' || carte.dataset.lieu === filtreLieu.value) &&
            (filtreArtiste.value === '' || carte.dataset.artiste === filtreArtiste.value);

        carte.hidden = !correspond;
    });
}

[filtreGenre, filtreLieu, filtreArtiste].forEach(filtre => filtre.addEventListener('change', filtrerVideos));
