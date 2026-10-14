// === Page d'accueil (Mode Lecture) ===
// Les tables (INTERVIEW, EXTRAIT, ARTISTE...) et les fonctions d'accès viennent de data.js,
// les fonctions d'affichage (creerElement, formaterTimecode...) de utils.js,
// la fenêtre modale (ouvrirInterview, ouvrirExtrait) de modal.js

// === Gestion du défilement (Navbar) ===
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 50));

// === Interview à la une ===
const interviewALaUne = trouver(INTERVIEW, 'id_interview', ID_INTERVIEW_A_LA_UNE);

function afficherInterviewALaUne() {
    const artiste = artisteDeInterview(interviewALaUne);
    const genres = genresDeArtiste(artiste);

    document.getElementById('hero').style.backgroundImage = `url('${artiste.photo_url}')`;
    document.getElementById('hero-title').textContent = artiste.nom_artiste;
    document.getElementById('hero-desc').textContent = interviewALaUne.description;

    const etiquetteGenres = creerElement('span');
    etiquetteGenres.append(...genres.map(creerPastille), ` ${nomsDesGenres(genres)}`);

    document.getElementById('hero-meta').replaceChildren(
        creerElement('span', null, `📍 ${texteLieu(lieuDeInterview(interviewALaUne))}`),
        etiquetteGenres
    );
}

afficherInterviewALaUne();
document.getElementById('hero-play').addEventListener('click', () => ouvrirInterview(interviewALaUne));

// === Cartes des vidéos ===
// Une carte représente un extrait ou une interview ; elle porte les identifiants
// de son artiste, de son lieu et de ses genres pour les filtres.
function creerCarte({ id, titre, type, image, interview, auClic }) {
    const artiste = artisteDeInterview(interview);
    const lieu = lieuDeInterview(interview);
    const genres = genresDeArtiste(artiste);

    const carte = creerElement('div', 'card');
    carte.id = id;
    carte.dataset.artiste = artiste.id_artiste;
    carte.dataset.lieu = lieu ? lieu.id_lieu : '';
    carte.dataset.genres = genres.map(genre => genre.id_genre).join(',');

    const miniature = creerElement('img');
    miniature.src = image;
    miniature.alt = 'Miniature';

    const etiquettes = creerElement('span', 'card-tags');
    etiquettes.append(...genres.map(creerPastille), ` ${type} • ${lieu ? lieu.ville : 'Lieu non précisé'}`);

    const infos = creerElement('div', 'card-info');
    infos.append(creerElement('span', 'card-title', titre), etiquettes);

    carte.append(miniature, infos);
    carte.addEventListener('click', auClic);
    return carte;
}

const carrouselExtraits = document.getElementById('extraits-carousel');
const carrouselInterviews = document.getElementById('interviews-carousel');

EXTRAIT.forEach(extrait => {
    carrouselExtraits.appendChild(creerCarte({
        id: `extrait-${extrait.id_extrait}`,
        titre: extrait.titre_extrait,
        type: 'Extrait',
        image: imageExtrait(extrait, 400, 225),
        interview: interviewDeExtrait(extrait),
        auClic: () => ouvrirExtrait(extrait)
    }));
});

INTERVIEW.forEach(interview => {
    carrouselInterviews.appendChild(creerCarte({
        id: `interview-${interview.id_interview}`,
        titre: interview.titre_interview,
        type: 'Intégrale',
        image: imageInterview(interview, 400, 225),
        interview,
        auClic: () => ouvrirInterview(interview)
    }));
});

// === Logique des filtres croisés de la base de données ===
const filtreGenre = document.getElementById('filter-genre');
const filtreLieu = document.getElementById('filter-lieu');
const filtreArtiste = document.getElementById('filter-artiste');
const cartes = document.querySelectorAll('.card');

function ajouterOptions(filtre, table, colonneId, texte) {
    table.forEach(ligne => {
        const option = creerElement('option', null, texte(ligne));
        option.value = ligne[colonneId];
        filtre.appendChild(option);
    });
}

ajouterOptions(filtreGenre, GENRE_MUSICAL, 'id_genre', genre => genre.nom_genre);
ajouterOptions(filtreLieu, LIEU, 'id_lieu', lieu => `${lieu.nom_lieu} (${lieu.ville})`);
ajouterOptions(filtreArtiste, ARTISTE, 'id_artiste', artiste => artiste.nom_artiste);

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
