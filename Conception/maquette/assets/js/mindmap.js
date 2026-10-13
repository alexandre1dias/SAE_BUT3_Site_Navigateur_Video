// === Page Carte Mentale (React) ===
// Les données (VIDEOS, ARTISTES, THEMES, GENRES) viennent de data.js

// === 1. Éléments de la carte ===
const ID_RACINE = 'racine';

// Rayon du cercle selon le type d'élément
const RAYONS = { racine: 34, artiste: 26, theme: 22, video: 14 };

// "couleur" correspond aux classes CSS noeud--xxx / lien--xxx de mindmap.css
const racine = { id: ID_RACINE, type: 'racine', couleur: 'racine', label: 'Base de données\nVidéos' };

const noeudsThemes = THEMES.map(theme => ({
    id: `theme-${theme.id}`,
    type: 'theme',
    couleur: 'theme',
    label: `Thème :\n${theme.nom}`
}));

const noeudsArtistes = ARTISTES.map(artiste => ({
    id: `artiste-${artiste.id}`,
    type: 'artiste',
    couleur: artiste.genre,
    label: `${artiste.nom}\n(${GENRES[artiste.genre].nom})`
}));

// Chaque vidéo appartient à un artiste et peut traiter d'un thème
const noeudsVideos = VIDEOS.map(video => ({
    id: video.id,
    type: 'video',
    couleur: 'video',
    label: video.titreCourt,
    artiste: `artiste-${video.artiste}`,
    theme: video.theme ? `theme-${video.theme}` : null
}));

const tousLesNoeuds = [racine, ...noeudsThemes, ...noeudsArtistes, ...noeudsVideos];

const noeudParId = {};
tousLesNoeuds.forEach(noeud => {
    noeud.rayon = RAYONS[noeud.type];
    noeud.lignes = noeud.label.split('\n');
    noeudParId[noeud.id] = noeud;
});

// === 2. Positions fixes ===
// Disposition en cercles autour du thème principal :
// thèmes sur le premier cercle, artistes sur le deuxième, vidéos sur le troisième.
const RAYON_THEMES = 230;
const RAYON_ARTISTES = 440;
const RAYON_VIDEOS = 700;
const ECART_VIDEOS = 22; // angle (en degrés) entre deux vidéos d'un même artiste
const MARGE = 90;

function placer(noeud, distance, angleDegres) {
    const angle = angleDegres * Math.PI / 180;
    noeud.x = Math.round(distance * Math.cos(angle));
    noeud.y = Math.round(distance * Math.sin(angle));
}

placer(racine, 0, 0);

noeudsThemes.forEach((theme, i) => {
    placer(theme, RAYON_THEMES, -45 + i * 360 / noeudsThemes.length);
});

noeudsArtistes.forEach((artiste, i) => {
    const angleArtiste = -90 + i * 360 / noeudsArtistes.length;
    placer(artiste, RAYON_ARTISTES, angleArtiste);

    // Les vidéos de l'artiste sont réparties en éventail derrière lui
    const sesVideos = noeudsVideos.filter(video => video.artiste === artiste.id);
    sesVideos.forEach((video, j) => {
        placer(video, RAYON_VIDEOS, angleArtiste + (j - (sesVideos.length - 1) / 2) * ECART_VIDEOS);
    });
});

// === 3. Liens ===
const liens = [];

[...noeudsArtistes, ...noeudsThemes].forEach(noeud => {
    liens.push({ from: ID_RACINE, to: noeud.id });
});

noeudsVideos.forEach(video => {
    liens.push({ from: video.artiste, to: video.id });
    if (video.theme) liens.push({ from: video.theme, to: video.id });
});

// Tracé de chaque lien : un segment allant du bord d'un élément au bord de l'autre
liens.forEach((lien, index) => {
    const depart = noeudParId[lien.from];
    const arrivee = noeudParId[lien.to];
    const dx = arrivee.x - depart.x;
    const dy = arrivee.y - depart.y;
    const longueur = Math.sqrt(dx * dx + dy * dy);
    const retraitDepart = depart.rayon + 3;
    const retraitArrivee = arrivee.rayon + 5;

    lien.id = index;
    lien.couleur = depart.couleur;
    lien.x1 = depart.x + dx / longueur * retraitDepart;
    lien.y1 = depart.y + dy / longueur * retraitDepart;
    lien.x2 = arrivee.x - dx / longueur * retraitArrivee;
    lien.y2 = arrivee.y - dy / longueur * retraitArrivee;
});

// Une pointe de flèche par couleur de lien
const couleursLiens = [...new Set(liens.map(lien => lien.couleur))];

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

// La vue est cadrée sur l'emplacement de la carte entièrement dépliée
const DEMI_COTE = RAYON_VIDEOS + MARGE;
const VIEW_BOX = [-DEMI_COTE, -DEMI_COTE, 2 * DEMI_COTE, 2 * DEMI_COTE].join(' ');

function Fleche({ couleur }) {
    return e('marker', {
        id: `fleche-${couleur}`,
        markerUnits: 'userSpaceOnUse',
        markerWidth: 10,
        markerHeight: 10,
        refX: 10,
        refY: 5,
        orient: 'auto'
    }, e('path', { d: 'M0,0 L10,5 L0,10 z', className: `fleche--${couleur}` }));
}

function Lien({ lien }) {
    return e('g', { className: `lien lien--${lien.couleur}` },
        e('line', {
            x1: lien.x1,
            y1: lien.y1,
            x2: lien.x2,
            y2: lien.y2,
            markerEnd: `url(#fleche-${lien.couleur})`
        })
    );
}

// Un élément ne réagit qu'au clic : aucun déplacement à la souris
function Noeud({ noeud, aDecouvrir, onBasculer }) {
    const classes = ['noeud', `noeud--${noeud.couleur}`];
    // Bordure en pointillés = il reste des éléments reliés à découvrir
    if (aDecouvrir) classes.push('noeud--a-decouvrir');

    return e('g', {
        className: classes.join(' '),
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
        e('defs', null, couleursLiens.map(couleur => e(Fleche, { key: couleur, couleur }))),
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
