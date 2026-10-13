// === Page d'accueil (Mode Lecture) ===
// Les tables (INTERVIEW, EXTRAIT, ARTISTE...) et les fonctions d'accès viennent de data.js,
// les fonctions d'affichage (creerElement, formaterTimecode...) de utils.js

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

// === Logique de la fenêtre Modale ===
const modal = document.getElementById('video-modal');
const choixLecteur = document.getElementById('player-source');

// Le lecteur proposé par défaut est celui préféré par l'utilisateur
choixLecteur.value = UTILISATEUR.lecteur_prefere;

// Vidéo affichée dans la modale : ses adresses et le timecode de départ
let lecture = null;

function ouvrirInterview(interview) {
    const extraits = extraitsDeInterview(interview);

    afficherModal({
        titre: interview.titre_interview,
        image: imageInterview(interview, 800, 450),
        description: interview.description,
        format: 'interview',
        interview,
        details: [
            ['Type de contenu', 'Interview Intégrale'],
            ['Tournage', interview.date_tournage ? formaterDate(interview.date_tournage) : 'Date non précisée'],
            ['Séquences', `${extraits.length} extraits`]
        ],
        // Bifurcations : les extraits de l'interview, dans l'ordre de la séquence
        liens: extraits.map(extrait => ({
            texte: `🔗 Aller à : ${extrait.titre_extrait}`,
            auClic: () => ouvrirExtrait(extrait)
        })),
        lecture: {
            YOUTUBE: interview.url_youtube,
            VIMEO: interview.url_vimeo,
            debut: 0
        }
    });
}

function ouvrirExtrait(extrait) {
    const interview = interviewDeExtrait(extrait);
    const question = questionDeExtrait(extrait);
    const theme = themeDeQuestion(question);

    // Bifurcations : la même question posée aux autres artistes, puis l'interview complète
    const memeQuestion = EXTRAIT.filter(autre =>
        autre.id_question === extrait.id_question && autre.id_extrait !== extrait.id_extrait
    );
    const liens = memeQuestion.map(autre => ({
        texte: `👤 Même question posée à ${artisteDeInterview(interviewDeExtrait(autre)).nom_artiste}`,
        auClic: () => ouvrirExtrait(autre)
    }));
    liens.push({
        texte: "▶️ Voir l'interview complète",
        auClic: () => ouvrirInterview(interview)
    });

    const fin = extrait.timecode_fin === null ? 'fin' : formaterTimecode(extrait.timecode_fin);

    afficherModal({
        titre: extrait.titre_extrait,
        image: imageExtrait(extrait, 800, 450),
        description: extrait.transcription,
        format: 'question',
        interview,
        details: [
            ['Type de contenu', 'Extrait / Réponse spécifique'],
            ['Thème', theme.titre_theme],
            ['Question', question.texte_question],
            ['Séquence', `n°${extrait.ordre_sequence} (${formaterTimecode(extrait.timecode_debut)} → ${fin})`]
        ],
        liens,
        // Sans vidéo propre à l'extrait, on lit l'interview à partir du timecode de début
        lecture: {
            YOUTUBE: extrait.url_youtube || interview.url_youtube,
            VIMEO: extrait.url_vimeo || interview.url_vimeo,
            debut: extrait.url_youtube || extrait.url_vimeo ? 0 : extrait.timecode_debut
        }
    });
}

function afficherModal(contenu) {
    const artiste = artisteDeInterview(contenu.interview);
    const genres = genresDeArtiste(artiste);
    const estInterview = contenu.format === 'interview';

    lecture = contenu.lecture;

    document.getElementById('modal-title').textContent = contenu.titre;
    document.getElementById('modal-desc').textContent = contenu.description;
    document.getElementById('modal-bg').style.backgroundImage = `url('${contenu.image}')`;
    document.getElementById('modal-location').textContent = `📍 ${texteLieu(lieuDeInterview(contenu.interview))}`;

    const badge = document.getElementById('modal-format-badge');
    badge.textContent = estInterview ? 'Interview Intégrale' : 'Extrait (Question)';
    badge.className = `format-badge ${contenu.format}`;

    // Fiche de la vidéo : artiste, couleur musicale, puis les détails propres au format
    const ligneGenres = creerElement('p');
    ligneGenres.append(
        creerElement('strong', null, 'Couleur musicale :'),
        creerElement('br'),
        ...genres.map(creerPastille),
        ` ${nomsDesGenres(genres)}`
    );

    const lignes = [['Artiste', artiste.nom_artiste], ...contenu.details].map(([libelle, valeur]) => {
        const ligne = creerElement('p');
        ligne.append(creerElement('strong', null, `${libelle} :`), ` ${valeur}`);
        return ligne;
    });

    document.getElementById('modal-meta').replaceChildren(lignes[0], ligneGenres, ...lignes.slice(1));

    // Un bouton par bifurcation possible depuis cette vidéo
    const boutons = contenu.liens.map(lien => {
        const bouton = creerElement('button', 'btn-related', lien.texte);
        bouton.addEventListener('click', () => {
            lien.auClic();
            document.querySelector('.modal-content').scrollTop = 0; // Remonte la modale tout en haut
        });
        return bouton;
    });
    document.getElementById('modal-related-links').replaceChildren(...boutons);

    modal.classList.add('active');
    document.body.classList.add('modal-ouverte');
}

function fermerModal() {
    modal.classList.remove('active');
    document.body.classList.remove('modal-ouverte');
}

function lancerVideo() {
    const lecteur = choixLecteur.value;
    const depart = lecture.debut ? ` (à partir de ${formaterTimecode(lecture.debut)})` : '';
    alert(`Lancement du lecteur vidéo via l'API : ${lecteur}\n${lecture[lecteur]}${depart}`);
}

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

// === Ouverture directe d'une vidéo ===
// Une adresse comme index.html#extrait-3 (lien depuis une playlist du profil) ouvre la vidéo correspondante
const carteCiblee = location.hash ? document.getElementById(location.hash.slice(1)) : null;
if (carteCiblee && carteCiblee.classList.contains('card')) carteCiblee.click();
