// === Page Carte Mentale (React) ===
// Les tables (ARTISTE, INTERVIEW, THEME, QUESTION, EXTRAIT...) et les fonctions d'accès viennent de data.js
//
// La carte suit les relations de la base :
//   racine → artiste → interview → extrait
//   racine → thème   → question  → extrait
// Un extrait est donc relié à la fois à son interview et à sa question.

// === 1. Éléments de la carte ===
const ID_RACINE = 'racine';
const COULEUR_PAR_DEFAUT = '#888888';

// Rayon du cercle selon le type d'élément
const RAYONS = { racine: 34, artiste: 26, theme: 24, interview: 20, question: 18, extrait: 13 };

// Découpe un texte en lignes courtes pour l'afficher sous un cercle
function couperEnLignes(texte, longueurMax = 22) {
    const lignes = [];
    texte.split(' ').forEach(mot => {
        const derniere = lignes[lignes.length - 1];
        if (derniere !== undefined && `${derniere} ${mot}`.length <= longueurMax) {
            lignes[lignes.length - 1] = `${derniere} ${mot}`;
        } else {
            lignes.push(mot);
        }
    });
    return lignes;
}

// Couleur d'un artiste : celle de son premier genre (genre_musical.code_couleur)
function couleurArtiste(artiste) {
    const genres = genresDeArtiste(artiste);
    return genres.length ? genres[0].code_couleur : COULEUR_PAR_DEFAUT;
}

// "couleur" n'est renseignée que si elle vient de la base ; sinon c'est la classe CSS noeud--<type> qui décide
const racine = { id: ID_RACINE, type: 'racine', label: 'Base de données Vidéos' };

const noeudsArtistes = ARTISTE.map(artiste => ({
    id: `artiste-${artiste.id_artiste}`,
    type: 'artiste',
    couleur: couleurArtiste(artiste),
    label: `${artiste.nom_artiste} (${genresDeArtiste(artiste).map(genre => genre.nom_genre).join(', ')})`
}));

const noeudsInterviews = INTERVIEW.map(interview => ({
    id: `interview-${interview.id_interview}`,
    type: 'interview',
    couleur: couleurArtiste(artisteDeInterview(interview)),
    label: interview.titre_interview,
    parent: `artiste-${interview.id_artiste}`
}));

const noeudsThemes = THEME.map(theme => ({
    id: `theme-${theme.id_theme}`,
    type: 'theme',
    label: `Thème : ${theme.titre_theme}`
}));

const noeudsQuestions = QUESTION.map(question => ({
    id: `question-${question.id_question}`,
    type: 'question',
    label: question.texte_question,
    parent: `theme-${question.id_theme}`
}));

// Les extraits sont rangés par interview puis par ordre de séquence
const noeudsExtraits = INTERVIEW.flatMap(extraitsDeInterview).map(extrait => ({
    id: `extrait-${extrait.id_extrait}`,
    type: 'extrait',
    label: extrait.titre_extrait,
    interview: `interview-${extrait.id_interview}`,
    question: `question-${extrait.id_question}`
}));

const tousLesNoeuds = [
    racine,
    ...noeudsArtistes,
    ...noeudsThemes,
    ...noeudsInterviews,
    ...noeudsQuestions,
    ...noeudsExtraits
];

const noeudParId = {};
tousLesNoeuds.forEach(noeud => {
    noeud.rayon = RAYONS[noeud.type];
    noeud.lignes = couperEnLignes(noeud.label);
    noeudParId[noeud.id] = noeud;
});

// === 2. Positions fixes ===
// Disposition en colonnes, de gauche à droite :
//   artistes | interviews | extraits | questions | thèmes
// La racine est en haut au centre ; les extraits, au milieu, font le lien entre les deux côtés.
function placerEnColonne(noeuds, x, yCentre, ecart) {
    noeuds.forEach((noeud, i) => {
        noeud.x = x;
        noeud.y = Math.round(yCentre + (i - (noeuds.length - 1) / 2) * ecart);
    });
}

racine.x = 0;
racine.y = -520;

placerEnColonne(noeudsArtistes, -620, -150, 220);
placerEnColonne(noeudsInterviews, -330, 120, 220);
placerEnColonne(noeudsExtraits, 0, 250, 105);
placerEnColonne(noeudsQuestions, 330, 150, 170);
placerEnColonne(noeudsThemes, 620, -150, 170);

// La vue est cadrée sur l'emplacement de la carte entièrement dépliée
const MARGE = 120;
const xs = tousLesNoeuds.map(noeud => noeud.x);
const ys = tousLesNoeuds.map(noeud => noeud.y);
const VIEW_BOX = [
    Math.min(...xs) - MARGE,
    Math.min(...ys) - MARGE,
    Math.max(...xs) - Math.min(...xs) + 2 * MARGE,
    Math.max(...ys) - Math.min(...ys) + 2 * MARGE
].join(' ');

// === 3. Liens ===
// Un lien par clé étrangère de la base
const liens = [];

[...noeudsArtistes, ...noeudsThemes].forEach(noeud => {
    liens.push({ from: ID_RACINE, to: noeud.id });
});

[...noeudsInterviews, ...noeudsQuestions].forEach(noeud => {
    liens.push({ from: noeud.parent, to: noeud.id });
});

noeudsExtraits.forEach(extrait => {
    liens.push({ from: extrait.interview, to: extrait.id });
    liens.push({ from: extrait.question, to: extrait.id });
});

// Tracé de chaque lien : un segment allant du bord d'un élément au bord de l'autre, terminé par une pointe de flèche
const LONGUEUR_POINTE = 10;
const DEMI_LARGEUR_POINTE = 5;

liens.forEach((lien, index) => {
    const depart = noeudParId[lien.from];
    const arrivee = noeudParId[lien.to];
    const dx = arrivee.x - depart.x;
    const dy = arrivee.y - depart.y;
    const longueur = Math.sqrt(dx * dx + dy * dy);
    // Vecteur unitaire dans le sens du lien
    const ux = dx / longueur;
    const uy = dy / longueur;

    lien.id = index;
    lien.type = depart.type;
    lien.couleur = depart.couleur;
    lien.x1 = depart.x + ux * (depart.rayon + 3);
    lien.y1 = depart.y + uy * (depart.rayon + 3);
    lien.x2 = arrivee.x - ux * (arrivee.rayon + 5);
    lien.y2 = arrivee.y - uy * (arrivee.rayon + 5);

    const baseX = lien.x2 - ux * LONGUEUR_POINTE;
    const baseY = lien.y2 - uy * LONGUEUR_POINTE;
    lien.pointe = [
        [lien.x2, lien.y2],
        [baseX - uy * DEMI_LARGEUR_POINTE, baseY + ux * DEMI_LARGEUR_POINTE],
        [baseX + uy * DEMI_LARGEUR_POINTE, baseY - ux * DEMI_LARGEUR_POINTE]
    ].map(point => point.join(',')).join(' ');
});

const voisinsDe = {};
tousLesNoeuds.forEach(noeud => { voisinsDe[noeud.id] = []; });
liens.forEach(lien => {
    voisinsDe[lien.from].push(lien.to);
    voisinsDe[lien.to].push(lien.from);
});

// === 4. Affichage progressif ===
// Un élément est visible s'il est atteignable depuis la racine en ne passant que par des éléments dépliés
function calculerVisibles(deplies) {
    const visibles = { [ID_RACINE]: true };
    const file = [ID_RACINE];
    while (file.length) {
        const id = file.shift();
        if (!deplies[id]) continue;
        voisinsDe[id].forEach(voisin => {
            if (!visibles[voisin]) {
                visibles[voisin] = true;
                file.push(voisin);
            }
        });
    }
    return visibles;
}

// === 5. Composants React ===
// Écrits avec React.createElement (sans JSX) pour fonctionner sans étape de compilation
const { useState, useRef } = React;
const e = React.createElement;

// Transmet au CSS une couleur venue de la base (sinon la classe du type s'applique)
function styleCouleur(couleur) {
    return couleur ? { '--couleur': couleur } : undefined;
}

function Lien({ lien }) {
    return e('g', { className: `lien lien--${lien.type}`, style: styleCouleur(lien.couleur) },
        e('line', { x1: lien.x1, y1: lien.y1, x2: lien.x2, y2: lien.y2 }),
        e('polygon', { points: lien.pointe })
    );
}

// Un élément ne réagit qu'au clic : aucun déplacement à la souris
function Noeud({ noeud, aDecouvrir, onBasculer }) {
    const classes = ['noeud', `noeud--${noeud.type}`];
    // Bordure en pointillés = il reste des éléments reliés à découvrir
    if (aDecouvrir) classes.push('noeud--a-decouvrir');

    return e('g', {
        className: classes.join(' '),
        style: styleCouleur(noeud.couleur),
        transform: `translate(${noeud.x} ${noeud.y})`,
        onPointerDown: event => event.stopPropagation(),
        onClick: () => onBasculer(noeud.id)
    },
        e('circle', { r: noeud.rayon }),
        e('text', { y: noeud.rayon + 20 },
            noeud.lignes.map((ligne, i) => e('tspan', { key: i, x: 0, dy: i === 0 ? 0 : 18 }, ligne))
        )
    );
}

function CarteMentale() {
    // Éléments dont les voisins sont affichés. Au départ aucun, donc seul le thème principal est visible.
    const [deplies, setDeplies] = useState({});
    // Zoom et décalage de la vue (les éléments, eux, ne bougent jamais)
    const [vue, setVue] = useState({ x: 0, y: 0, zoom: 1 });
    const [enDeplacement, setEnDeplacement] = useState(false);
    const svg = useRef(null);
    const depart = useRef(null);

    const visibles = calculerVisibles(deplies);
    const noeudsVisibles = tousLesNoeuds.filter(noeud => visibles[noeud.id]);
    const liensVisibles = liens.filter(lien => visibles[lien.from] && visibles[lien.to]);

    // Un clic affiche les éléments reliés, un second clic les replie
    function basculer(id) {
        setDeplies(precedents => {
            const suivants = { ...precedents };
            if (suivants[id]) delete suivants[id];
            else suivants[id] = true;

            // Un élément masqué perd son état déplié
            const encoreVisibles = calculerVisibles(suivants);
            Object.keys(suivants).forEach(cle => {
                if (!encoreVisibles[cle]) delete suivants[cle];
            });
            return suivants;
        });
    }

    // Convertit la position de la souris en coordonnées de la carte
    function positionSouris(event) {
        const matrice = svg.current.getScreenCTM().inverse();
        return new DOMPoint(event.clientX, event.clientY).matrixTransform(matrice);
    }

    // Zoom centré sur la position de la souris
    function zoomer(event) {
        const souris = positionSouris(event);
        const sens = event.deltaY < 0 ? 1.15 : 1 / 1.15;
        setVue(actuelle => {
            const zoom = Math.min(4, Math.max(0.4, actuelle.zoom * sens));
            const facteur = zoom / actuelle.zoom;
            return {
                x: souris.x - (souris.x - actuelle.x) * facteur,
                y: souris.y - (souris.y - actuelle.y) * facteur,
                zoom
            };
        });
    }

    function debuterDeplacement(event) {
        depart.current = { souris: positionSouris(event), x: vue.x, y: vue.y };
        setEnDeplacement(true);
        svg.current.setPointerCapture(event.pointerId);
    }

    function deplacer(event) {
        if (!enDeplacement) return;
        const souris = positionSouris(event);
        const origine = depart.current;
        setVue(actuelle => ({
            ...actuelle,
            x: origine.x + souris.x - origine.souris.x,
            y: origine.y + souris.y - origine.souris.y
        }));
    }

    function terminerDeplacement() {
        setEnDeplacement(false);
    }

    return e('svg', {
        ref: svg,
        className: enDeplacement ? 'carte en-deplacement' : 'carte',
        viewBox: VIEW_BOX,
        onWheel: zoomer,
        onPointerDown: debuterDeplacement,
        onPointerMove: deplacer,
        onPointerUp: terminerDeplacement,
        onPointerCancel: terminerDeplacement
    },
        e('g', { transform: `translate(${vue.x} ${vue.y}) scale(${vue.zoom})` },
            liensVisibles.map(lien => e(Lien, { key: lien.id, lien })),
            noeudsVisibles.map(noeud => e(Noeud, {
                key: noeud.id,
                noeud,
                aDecouvrir: voisinsDe[noeud.id].some(voisin => !visibles[voisin]),
                onBasculer: basculer
            }))
        )
    );
}

ReactDOM.createRoot(document.getElementById('app')).render(e(CarteMentale));
