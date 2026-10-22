// === Fenêtre modale d'une vidéo (interview ou extrait) ===
// Partagée par la page d'accueil et la carte mentale.
// À charger après data.js et utils.js ; la page doit contenir le HTML de la modale (#video-modal).

const modal = document.getElementById('video-modal');
const choixLecteur = document.getElementById('player-source');

// Vidéo affichée dans la modale : ses adresses et le timecode de départ
let lecture = null;

function ouvrirInterview(interview) {
    const extraits = extraitsDeInterview(interview);

    afficherModal({
        titre: interview.titreInterview,
        image: imageInterview(interview, 800, 450),
        description: interview.descriptionInterview,
        format: 'interview',
        interview,
        details: [
            ['Type de contenu', 'Interview Intégrale'],
            ['Tournage', interview.dateTournage ? formaterDate(interview.dateTournage) : 'Date non précisée'],
            ['Séquences', `${extraits.length} extraits`]
        ],
        // Bifurcations : les extraits de l'interview, dans l'ordre de la séquence
        liens: extraits.map(extrait => ({
            texte: `🔗 Aller à : ${extrait.titreExtrait}`,
            auClic: () => ouvrirExtrait(extrait)
        })),
        lecture: {
            YOUTUBE: interview.urlYoutube,
            VIMEO: interview.urlVimeo,
            debut: 0
        }
    });
}

function ouvrirExtrait(extrait) {
    const interview = interviewDeExtrait(extrait);
    const question = questionDeExtrait(extrait);

    // Bifurcations : la même question posée aux autres artistes, puis l'interview complète
    const memeQuestion = EXTRAIT.filter(autre =>
        autre.question_id === extrait.question_id && autre.idExtrait !== extrait.idExtrait
    );
    const liens = memeQuestion.map(autre => ({
        texte: `👤 Même question posée à ${artisteDeInterview(interviewDeExtrait(autre)).nomArtiste}`,
        auClic: () => ouvrirExtrait(autre)
    }));
    liens.push({
        texte: "▶️ Voir l'interview complète",
        auClic: () => ouvrirInterview(interview)
    });

    const fin = extrait.timecodeFin === null ? 'fin' : formaterTimecode(extrait.timecodeFin);

    afficherModal({
        titre: extrait.titreExtrait,
        image: imageExtrait(extrait, 800, 450),
        description: extrait.transcription,
        format: 'question',
        interview,
        details: [
            ['Type de contenu', 'Extrait / Réponse spécifique'],
            ['Question', question.texteQuestion],
            ['Séquence', `n°${extrait.ordreSequence} (${formaterTimecode(extrait.timecodeDebut)} → ${fin})`]
        ],
        liens,
        // Sans vidéo propre à l'extrait, on lit l'interview à partir du timecode de début
        lecture: {
            YOUTUBE: extrait.urlYoutube || interview.urlYoutube,
            VIMEO: extrait.urlVimeo || interview.urlVimeo,
            debut: extrait.urlYoutube || extrait.urlVimeo ? 0 : extrait.timecodeDebut
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

    const lignes = [['Artiste', artiste.nomArtiste], ...contenu.details].map(([libelle, valeur]) => {
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
