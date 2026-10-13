// === Données de la maquette ===
// Jeu de données fictif qui reprend la structure de la base de données :
// une constante par table, une propriété par colonne (mêmes noms que dans le SQL).
// Dans le site final, ces données viendront de l'API.

const GENRE_MUSICAL = [
    { id_genre: 1, nom_genre: 'Rock', code_couleur: '#E50914' },
    { id_genre: 2, nom_genre: 'Électro-Pop', code_couleur: '#3578e5' },
    { id_genre: 3, nom_genre: 'Rap', code_couleur: '#46d369' }
];

const ARTISTE = [
    {
        id_artiste: 1,
        nom_artiste: 'Artiste A',
        biographie: 'Guitariste et chanteur, figure de la scène rock lyonnaise.',
        photo_url: 'https://picsum.photos/1920/1080?random=11'
    },
    {
        id_artiste: 2,
        nom_artiste: 'Artiste B',
        biographie: 'Producteur et compositeur, entre machines et mélodies pop.',
        photo_url: 'https://picsum.photos/1920/1080?random=10'
    },
    {
        id_artiste: 3,
        nom_artiste: 'Artiste C',
        biographie: 'Rappeur et auteur, habitué des scènes de festival.',
        photo_url: 'https://picsum.photos/1920/1080?random=12'
    }
];

// Un artiste peut avoir plusieurs genres
const ARTISTE_GENRE = [
    { id_artiste: 1, id_genre: 1 },
    { id_artiste: 2, id_genre: 2 },
    { id_artiste: 3, id_genre: 3 }
];

const LIEU = [
    { id_lieu: 1, nom_lieu: 'Le Transbordeur', ville: 'Lyon', pays: 'France' },
    { id_lieu: 2, nom_lieu: 'Studio La Seine', ville: 'Paris', pays: 'France' },
    { id_lieu: 3, nom_lieu: 'Les Eurockéennes', ville: 'Belfort', pays: 'France' }
];

const THEME = [
    { id_theme: 1, titre_theme: 'Processus créatif', description_theme: "Comment naissent les morceaux, de l'idée à l'enregistrement." },
    { id_theme: 2, titre_theme: 'Gérer la pression', description_theme: 'Les attentes du public, le stress et la façon de les apprivoiser.' },
    { id_theme: 3, titre_theme: 'Anecdotes de tournée', description_theme: 'La vie sur la route, entre deux concerts.' },
    { id_theme: 4, titre_theme: 'Le trac', description_theme: 'Les minutes qui précèdent la montée sur scène.' }
];

// Chaque question appartient à un thème
const QUESTION = [
    { id_question: 1, texte_question: 'Comment naît un morceau chez vous ?', description_question: 'Méthode de composition et sources d\'inspiration.', id_theme: 1 },
    { id_question: 2, texte_question: 'Comment gérez-vous la pression ?', description_question: 'Rapport aux attentes du public et de la profession.', id_theme: 2 },
    { id_question: 3, texte_question: 'Quel est votre meilleur souvenir de tournée ?', description_question: null, id_theme: 3 },
    { id_question: 4, texte_question: 'Avez-vous le trac avant de monter sur scène ?', description_question: 'Rituels et préparation avant un concert.', id_theme: 4 }
];

// Une interview = un artiste filmé dans un lieu (id_lieu peut être null)
const INTERVIEW = [
    {
        id_interview: 1,
        titre_interview: 'Artiste A - Intégrale',
        date_tournage: '2026-03-14',
        description: "L'interview complète de l'Artiste A. Sans coupure.",
        url_youtube: 'https://www.youtube.com/watch?v=interview-a',
        url_vimeo: 'https://vimeo.com/100000001',
        id_artiste: 1,
        id_lieu: 1
    },
    {
        id_interview: 2,
        titre_interview: 'Artiste B - Intégrale',
        date_tournage: '2026-04-02',
        description: "Rencontre intimiste au Studio La Seine avec l'Artiste B, qui revient sur la création de son dernier album.",
        url_youtube: 'https://www.youtube.com/watch?v=interview-b',
        url_vimeo: 'https://vimeo.com/100000002',
        id_artiste: 2,
        id_lieu: 2
    },
    {
        id_interview: 3,
        titre_interview: 'Artiste C - Intégrale',
        date_tournage: '2026-07-05',
        description: 'Artiste C se confie en plein air lors de son dernier festival estival.',
        url_youtube: 'https://www.youtube.com/watch?v=interview-c',
        url_vimeo: 'https://vimeo.com/100000003',
        id_artiste: 3,
        id_lieu: 3
    }
];

// Un extrait = la réponse à une question, découpée dans une interview.
// timecode_debut / timecode_fin sont en secondes.
// url_youtube / url_vimeo à null : on lit la vidéo de l'interview à partir de timecode_debut.
const EXTRAIT = [
    {
        id_extrait: 1,
        titre_extrait: 'Le processus créatif (Artiste A)',
        ordre_sequence: 1,
        timecode_debut: 0,
        timecode_fin: 312,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« Tout part d'un riff de guitare. Je l'enregistre sur mon téléphone, et s'il me reste en tête le lendemain, j'en fais un morceau. »",
        id_interview: 1,
        id_question: 1
    },
    {
        id_extrait: 2,
        titre_extrait: 'Gérer la pression (Artiste A)',
        ordre_sequence: 2,
        timecode_debut: 312,
        timecode_fin: 655,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« Le public rock attend qu'on se donne à fond chaque soir. La pression, je la transforme en énergie. »",
        id_interview: 1,
        id_question: 2
    },
    {
        id_extrait: 3,
        titre_extrait: 'Souvenirs de tournée (Artiste A)',
        ordre_sequence: 3,
        timecode_debut: 655,
        timecode_fin: 1020,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« Le pire comme le meilleur : une panne de bus en pleine nuit, et un concert improvisé sur une aire d'autoroute. »",
        id_interview: 1,
        id_question: 3
    },
    {
        id_extrait: 4,
        titre_extrait: 'Le processus créatif (Artiste B)',
        ordre_sequence: 1,
        timecode_debut: 0,
        timecode_fin: 280,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« Je commence toujours par un son sur mes machines. La mélodie vient après, presque par accident. »",
        id_interview: 2,
        id_question: 1
    },
    {
        id_extrait: 5,
        titre_extrait: 'Gérer la pression (Artiste B)',
        ordre_sequence: 2,
        timecode_debut: 280,
        timecode_fin: 610,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« Sur les grandes scènes électro, le stress est énorme. J'ai appris à respirer et à faire confiance à mon set. »",
        id_interview: 2,
        id_question: 2
    },
    {
        id_extrait: 6,
        titre_extrait: 'Le processus créatif (Artiste C)',
        ordre_sequence: 1,
        timecode_debut: 0,
        timecode_fin: 295,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« J'écris dans le métro, dans la rue. La ville me donne les mots, je n'ai plus qu'à les mettre en rythme. »",
        id_interview: 3,
        id_question: 1
    },
    {
        id_extrait: 7,
        titre_extrait: 'Le trac avant la scène (Artiste C)',
        ordre_sequence: 2,
        timecode_debut: 295,
        timecode_fin: 540,
        url_youtube: null,
        url_vimeo: null,
        transcription: "« Avant chaque concert j'ai le même rituel : cinq minutes seul, sans téléphone. Sans ça, impossible de monter sur scène. »",
        id_interview: 3,
        id_question: 4
    }
];

// Utilisateur connecté dans la maquette (pas de mot de passe ici : il reste côté serveur)
const UTILISATEUR = {
    id_utilisateur: 1,
    nom_utilisateur: 'demo',
    email: 'demo@example.com',
    lecteur_prefere: 'YOUTUBE'
};

const PLAYLIST = [
    { id_playlist: 1, titre_playlist: 'Mes extraits préférés', date_creation: '2026-09-12 18:30:00', id_utilisateur: 1 },
    { id_playlist: 2, titre_playlist: 'Spécial processus créatif', date_creation: '2026-10-01 09:15:00', id_utilisateur: 1 }
];

// Extraits d'une playlist, rangés par position
const PLAYLIST_EXTRAIT = [
    { id_playlist: 1, id_extrait: 2, position: 1 },
    { id_playlist: 1, id_extrait: 7, position: 2 },
    { id_playlist: 1, id_extrait: 3, position: 3 },
    { id_playlist: 2, id_extrait: 1, position: 1 },
    { id_playlist: 2, id_extrait: 4, position: 2 },
    { id_playlist: 2, id_extrait: 6, position: 3 }
];

// Choix propre à la maquette (hors base de données) : interview mise en avant sur l'accueil
const ID_INTERVIEW_A_LA_UNE = 2;

// === Fonctions d'accès aux données ===
// Elles jouent le rôle des jointures SQL entre les tables.

function trouver(table, colonne, valeur) {
    return table.find(ligne => ligne[colonne] === valeur);
}

function artisteDeInterview(interview) {
    return trouver(ARTISTE, 'id_artiste', interview.id_artiste);
}

function lieuDeInterview(interview) {
    return trouver(LIEU, 'id_lieu', interview.id_lieu) || null;
}

function genresDeArtiste(artiste) {
    return ARTISTE_GENRE
        .filter(lien => lien.id_artiste === artiste.id_artiste)
        .map(lien => trouver(GENRE_MUSICAL, 'id_genre', lien.id_genre));
}

// Extraits d'une interview, dans l'ordre de la séquence
function extraitsDeInterview(interview) {
    return EXTRAIT
        .filter(extrait => extrait.id_interview === interview.id_interview)
        .sort((a, b) => a.ordre_sequence - b.ordre_sequence);
}

function interviewDeExtrait(extrait) {
    return trouver(INTERVIEW, 'id_interview', extrait.id_interview);
}

function questionDeExtrait(extrait) {
    return trouver(QUESTION, 'id_question', extrait.id_question);
}

function themeDeQuestion(question) {
    return trouver(THEME, 'id_theme', question.id_theme);
}

function playlistsDeUtilisateur(utilisateur) {
    return PLAYLIST.filter(playlist => playlist.id_utilisateur === utilisateur.id_utilisateur);
}

// Extraits d'une playlist, dans l'ordre choisi par l'utilisateur
function extraitsDePlaylist(playlist) {
    return PLAYLIST_EXTRAIT
        .filter(lien => lien.id_playlist === playlist.id_playlist)
        .sort((a, b) => a.position - b.position)
        .map(lien => trouver(EXTRAIT, 'id_extrait', lien.id_extrait));
}
