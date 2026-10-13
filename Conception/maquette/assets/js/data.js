// === Données de la maquette ===
// Jeu de données fictif partagé par les deux pages (Mode Lecture et Mode Carte Mentale).
// Dans le site final, ces données viendront de l'API.

const GENRES = {
    rock: { nom: 'Rock', nomComplet: 'Rock' },
    electro: { nom: 'Électro', nomComplet: 'Électro-Pop' },
    rap: { nom: 'Rap', nomComplet: 'Rap' }
};

const LIEUX = {
    paris: 'Paris',
    lyon: 'Lyon',
    festival: 'Festival'
};

const ARTISTES = [
    { id: 'a', nom: 'Artiste A', genre: 'rock' },
    { id: 'b', nom: 'Artiste B', genre: 'electro' },
    { id: 'c', nom: 'Artiste C', genre: 'rap' }
];

const THEMES = [
    { id: 'processus', nom: 'Processus Créatif' },
    { id: 'pression', nom: 'Gérer la Pression' },
    { id: 'tournee', nom: 'Anecdotes Tournée' },
    { id: 'trac', nom: 'Le Trac' }
];

// format : 'question' (extrait sur un thème) ou 'interview' (intégrale)
// image  : numéro de l'image d'illustration (picsum.photos)
// liens  : bifurcations proposées depuis la vidéo
const VIDEOS = [
    // --- Thème : le processus créatif ---
    {
        id: 'vid-processus-a',
        titre: 'Le processus créatif (Artiste A)',
        titreCourt: 'Processus A',
        description: "L'Artiste A nous explique comment il compose ses riffs de guitare.",
        format: 'question',
        artiste: 'a',
        theme: 'processus',
        lieu: 'lyon',
        image: 200,
        liens: [
            { cible: 'vid-processus-b', texte: "👤 Même question posée à l'Artiste B" },
            { cible: 'vid-processus-c', texte: "👤 Même question posée à l'Artiste C" },
            { cible: 'vid-integrale-a', texte: "▶️ Voir l'interview complète" }
        ]
    },
    {
        id: 'vid-processus-b',
        titre: 'Le processus créatif (Artiste B)',
        titreCourt: 'Processus B',
        description: "L'Artiste B partage ses secrets de fabrication sur ses machines.",
        format: 'question',
        artiste: 'b',
        theme: 'processus',
        lieu: 'paris',
        image: 201,
        liens: [
            { cible: 'vid-processus-a', texte: "👤 Même question posée à l'Artiste A" },
            { cible: 'vid-processus-c', texte: "👤 Même question posée à l'Artiste C" },
            { cible: 'vid-integrale-b', texte: "▶️ Voir l'interview complète" }
        ]
    },
    {
        id: 'vid-processus-c',
        titre: 'Le processus créatif (Artiste C)',
        titreCourt: 'Processus C',
        description: "L'Artiste C parle de son écriture et de ses inspirations urbaines.",
        format: 'question',
        artiste: 'c',
        theme: 'processus',
        lieu: 'festival',
        image: 202,
        liens: [
            { cible: 'vid-processus-a', texte: "👤 Même question posée à l'Artiste A" },
            { cible: 'vid-processus-b', texte: "👤 Même question posée à l'Artiste B" },
            { cible: 'vid-integrale-c', texte: "▶️ Voir l'interview complète" }
        ]
    },

    // --- Thème : gérer la pression ---
    {
        id: 'vid-pression-a',
        titre: 'Gérer la pression (Artiste A)',
        titreCourt: 'Pression A',
        description: "Comment faire face aux attentes du public rock ? L'Artiste A témoigne.",
        format: 'question',
        artiste: 'a',
        theme: 'pression',
        lieu: 'lyon',
        image: 210,
        liens: [
            { cible: 'vid-pression-b', texte: "👤 Même question posée à l'Artiste B" },
            { cible: 'vid-integrale-a', texte: "▶️ Voir l'interview complète" }
        ]
    },
    {
        id: 'vid-pression-b',
        titre: 'Gérer la pression (Artiste B)',
        titreCourt: 'Pression B',
        description: "L'Artiste B se confie sur le stress des grandes scènes électro.",
        format: 'question',
        artiste: 'b',
        theme: 'pression',
        lieu: 'paris',
        image: 211,
        liens: [
            { cible: 'vid-pression-a', texte: "👤 Même question posée à l'Artiste A" },
            { cible: 'vid-integrale-b', texte: "▶️ Voir l'interview complète" }
        ]
    },

    // --- Autres thèmes ---
    {
        id: 'vid-trac-c',
        titre: 'Le trac avant la scène (Artiste C)',
        titreCourt: 'Trac C',
        description: 'Artiste C nous parle de son rituel avant de monter sur scène en festival.',
        format: 'question',
        artiste: 'c',
        theme: 'trac',
        lieu: 'festival',
        image: 22,
        liens: [
            { cible: 'vid-integrale-c', texte: "▶️ Voir l'interview complète d'Artiste C" }
        ]
    },
    {
        id: 'vid-tournee-a',
        titre: 'Souvenirs de tournée (Artiste A)',
        titreCourt: 'Tournée A',
        description: "Les pires et meilleures anecdotes de tournée de l'Artiste A.",
        format: 'question',
        artiste: 'a',
        theme: 'tournee',
        lieu: 'paris',
        image: 23,
        liens: [
            { cible: 'vid-integrale-a', texte: "▶️ Voir l'interview complète" }
        ]
    },

    // --- Interviews complètes ---
    {
        id: 'vid-integrale-a',
        titre: 'Artiste A - Intégrale',
        titreCourt: 'Intégrale A',
        description: "L'interview complète de l'Artiste A. Sans coupure.",
        format: 'interview',
        artiste: 'a',
        lieu: 'lyon',
        duree: '45 min',
        image: 30,
        liens: [
            { cible: 'vid-processus-a', texte: '🔗 Aller à : Le processus créatif' },
            { cible: 'vid-pression-a', texte: '🔗 Aller à : Gérer la pression' },
            { cible: 'vid-tournee-a', texte: '🔗 Aller à : Souvenirs de tournée' }
        ]
    },
    {
        id: 'vid-integrale-b',
        titre: 'Artiste B - Intégrale',
        titreCourt: 'Intégrale B',
        description: "Rencontre intimiste au Studio La Seine avec l'Artiste B.",
        format: 'interview',
        artiste: 'b',
        lieu: 'paris',
        duree: '52 min',
        image: 31,
        liens: [
            { cible: 'vid-processus-b', texte: '🔗 Aller à : Le processus créatif' },
            { cible: 'vid-pression-b', texte: '🔗 Aller à : Gérer la pression' }
        ]
    },
    {
        id: 'vid-integrale-c',
        titre: 'Artiste C - Intégrale',
        titreCourt: 'Intégrale C',
        description: 'Artiste C se confie en plein air lors de son dernier festival estival.',
        format: 'interview',
        artiste: 'c',
        lieu: 'festival',
        duree: '38 min',
        image: 32,
        liens: [
            { cible: 'vid-processus-c', texte: '🔗 Aller à : Le processus créatif' },
            { cible: 'vid-trac-c', texte: '🔗 Aller à : Le trac avant la scène' }
        ]
    }
];

// Vidéo mise en avant en haut de la page d'accueil
const VIDEO_A_LA_UNE = {
    titre: 'Artiste B - Interview Complète',
    description: "Découvrez l'interview exclusive de l'Artiste B. Un échange sans filtre sur la création et la tournée.",
    format: 'interview',
    artiste: 'b',
    lieuTexte: 'Studio La Seine, Paris',
    imageModale: 'https://picsum.photos/1920/1080?random=10',
    liens: [
        { cible: 'vid-processus-b', texte: '🔗 Bifurquer vers : Le processus créatif' },
        { cible: 'vid-pression-b', texte: '🔗 Bifurquer vers : Gérer la pression' }
    ]
};
