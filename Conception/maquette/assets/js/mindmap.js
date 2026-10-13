// === Page Carte Mentale (Vue.js) ===
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
    liens.push({ from: video.artiste, to: video.id, label: 'A_POUR_VIDEO' });
    if (video.theme) liens.push({ from: video.theme, to: video.id, label: 'PARLE_DE' });
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
    const angle = Math.atan2(dy, dx) * 180 / Math.PI;

    lien.id = index;
    lien.couleur = depart.couleur;
    lien.x1 = depart.x + dx / longueur * retraitDepart;
    lien.y1 = depart.y + dy / longueur * retraitDepart;
    lien.x2 = arrivee.x - dx / longueur * retraitArrivee;
    lien.y2 = arrivee.y - dy / longueur * retraitArrivee;
    lien.milieuX = (lien.x1 + lien.x2) / 2;
    lien.milieuY = (lien.y1 + lien.y2) / 2;
    // Le texte du lien suit le segment sans jamais être à l'envers
    lien.angle = angle > 90 || angle < -90 ? angle + 180 : angle;
});

// Une pointe de flèche par couleur de lien
const couleursLiens = [...new Set(liens.map(lien => lien.couleur))];

const voisinsDe = {};
tousLesNoeuds.forEach(noeud => { voisinsDe[noeud.id] = []; });
liens.forEach(lien => {
    voisinsDe[lien.from].push(lien.to);
    voisinsDe[lien.to].push(lien.from);
});

// === 4. Application Vue ===
// Le gabarit (#gabarit-carte) se trouve dans mindmap.html
Vue.createApp({
    template: '#gabarit-carte',

    data() {
        return {
            couleursLiens,
            // Affichage progressif : éléments dont les voisins sont affichés.
            // Au départ aucun, donc seul le thème principal est visible.
            deplies: {},
            // Zoom et décalage de la vue (les éléments, eux, ne bougent jamais)
            vue: { x: 0, y: 0, zoom: 1 },
            enDeplacement: false
        };
    },

    computed: {
        // La vue est cadrée sur l'emplacement de la carte entièrement dépliée
        viewBox() {
            const demiCote = RAYON_VIDEOS + MARGE;
            return [-demiCote, -demiCote, 2 * demiCote, 2 * demiCote].join(' ');
        },

        transformationVue() {
            return `translate(${this.vue.x} ${this.vue.y}) scale(${this.vue.zoom})`;
        },

        // Un élément est visible s'il est atteignable depuis la racine en ne passant que par des éléments dépliés
        visibles() {
            const visibles = { [ID_RACINE]: true };
            const file = [ID_RACINE];
            while (file.length) {
                const id = file.shift();
                if (!this.deplies[id]) continue;
                voisinsDe[id].forEach(voisin => {
                    if (!visibles[voisin]) {
                        visibles[voisin] = true;
                        file.push(voisin);
                    }
                });
            }
            return visibles;
        },

        noeudsVisibles() {
            return tousLesNoeuds.filter(noeud => this.visibles[noeud.id]);
        },

        liensVisibles() {
            return liens.filter(lien => this.visibles[lien.from] && this.visibles[lien.to]);
        }
    },

    methods: {
        // Un clic affiche les éléments reliés, un second clic les replie
        basculer(id) {
            if (this.deplies[id]) delete this.deplies[id];
            else this.deplies[id] = true;

            // Un élément masqué perd son état déplié
            Object.keys(this.deplies).forEach(cle => {
                if (!this.visibles[cle]) delete this.deplies[cle];
            });
        },

        // Vrai s'il reste des éléments reliés à découvrir (bordure en pointillés)
        resteADecouvrir(id) {
            return voisinsDe[id].some(voisin => !this.visibles[voisin]);
        },

        // Convertit la position de la souris en coordonnées de la carte
        positionSouris(event) {
            const matrice = this.$refs.svg.getScreenCTM().inverse();
            return new DOMPoint(event.clientX, event.clientY).matrixTransform(matrice);
        },

        // Zoom centré sur la position de la souris
        zoomer(event) {
            const souris = this.positionSouris(event);
            const zoomVoulu = this.vue.zoom * (event.deltaY < 0 ? 1.15 : 1 / 1.15);
            const zoom = Math.min(4, Math.max(0.4, zoomVoulu));
            const facteur = zoom / this.vue.zoom;
            this.vue.x = souris.x - (souris.x - this.vue.x) * facteur;
            this.vue.y = souris.y - (souris.y - this.vue.y) * facteur;
            this.vue.zoom = zoom;
        },

        debuterDeplacement(event) {
            this.depart = { souris: this.positionSouris(event), x: this.vue.x, y: this.vue.y };
            this.enDeplacement = true;
            this.$refs.svg.setPointerCapture(event.pointerId);
        },

        deplacer(event) {
            if (!this.enDeplacement) return;
            const souris = this.positionSouris(event);
            this.vue.x = this.depart.x + souris.x - this.depart.souris.x;
            this.vue.y = this.depart.y + souris.y - this.depart.souris.y;
        },

        terminerDeplacement() {
            this.enDeplacement = false;
        }
    }
}).mount('#app');
