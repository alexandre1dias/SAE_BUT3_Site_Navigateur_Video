const graph = document.getElementById('mindmap-graph');
const nodesContainer = document.getElementById('mindmap-nodes');
const lines = document.getElementById('mindmap-lines');
const detailsTitle = document.getElementById('details-title');
const detailsDescription = document.getElementById('details-description');
const detailsRelations = document.getElementById('details-relations');
const searchInput = document.getElementById('mindmap-keywords');
const dateFrom = document.getElementById('mindmap-date-from');
const dateTo = document.getElementById('mindmap-date-to');
const result = document.getElementById('mindmap-result');
const data = [...document.querySelectorAll('#mindmap-data .map-data')].map(element => ({
    ...element.dataset,
    relations: element.dataset.relations ? element.dataset.relations.split(',').filter(Boolean) : [],
}));
const byId = new Map(data.map(node => [node.id, node]));
let activeType = 'all';
let selectedId = null;
let zoom = 1;
let carteOuverte = false;
const navigation = [];

const typeNames = {
    artiste: 'Artiste', lieu: 'Lieu', genre: 'Genre', question: 'Question',
    interview: 'Interview', extrait: 'Extrait',
};

function normaliserRecherche(texte) {
    return texte
        .toLocaleLowerCase('fr-FR')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
}

function matches(node) {
    const words = normaliserRecherche(searchInput.value).trim().split(/\s+/).filter(Boolean);
    const textMatch = words.every(word => normaliserRecherche(node.search || '').includes(word));
    const dateMatch = (!dateFrom.value || (node.date && node.date >= dateFrom.value))
        && (!dateTo.value || (node.date && node.date <= dateTo.value));
    return textMatch && dateMatch && (activeType === 'all' || node.type === activeType);
}

function relatedTo(node) {
    return node.relations.map(id => byId.get(id)).filter(Boolean);
}

function showDetails(node, ajouterHistorique = true) {
    if (ajouterHistorique && selectedId && selectedId !== node.id) {
        navigation.push(selectedId);
    }
    carteOuverte = true;
    selectedId = node.id;
    const relations = relatedTo(node);
    detailsTitle.textContent = node.label;
    detailsDescription.textContent = `${typeNames[node.type]} · ${relations.length} relation${relations.length > 1 ? 's' : ''}`;
    detailsRelations.replaceChildren();
    if (node.fiche) {
        const openButton = document.createElement('button');
        openButton.type = 'button';
        openButton.className = 'relation relation--open';
        openButton.dataset.fiche = node.fiche;
        openButton.textContent = '▶ Ouvrir la vidéo';
        detailsRelations.appendChild(openButton);
    }
    relations.forEach(relation => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `relation relation--${relation.type}`;
        button.textContent = `${relation.type === 'interview' || relation.type === 'extrait' ? '▶ ' : ''}${relation.label}`;
        if (relation.fiche) {
            button.dataset.fiche = relation.fiche;
        } else {
            button.addEventListener('click', () => {
                showDetails(relation);
                render();
            });
        }
        detailsRelations.appendChild(button);
    });
    render();
}

function layout(visible) {
    const center = { x: 50, y: 50 };
    const metadata = visible.filter(node => ['artiste', 'lieu', 'genre', 'question'].includes(node.type));
    const videos = visible.filter(node => ['interview', 'extrait'].includes(node.type));
    const positions = new Map();
    positions.set('root', center);
    metadata.forEach((node, index) => {
        const angle = -Math.PI / 2 + (index / Math.max(metadata.length, 1)) * Math.PI * 2;
        positions.set(node.id, { x: 50 + Math.cos(angle) * 34, y: 50 + Math.sin(angle) * 34 });
    });
    videos.forEach((node, index) => {
        const angle = -Math.PI / 2 + (index / Math.max(videos.length, 1)) * Math.PI * 2;
        positions.set(node.id, { x: 50 + Math.cos(angle) * 18, y: 50 + Math.sin(angle) * 18 });
    });
    return positions;
}

function render() {
    const searchActive = searchInput.value.trim() || dateFrom.value || dateTo.value || activeType !== 'all';
    let visible = carteOuverte ? data.filter(matches) : [];
    if (carteOuverte && !searchActive && !selectedId) {
        visible = data.filter(node => ['artiste', 'lieu', 'genre', 'question'].includes(node.type));
    } else if (carteOuverte && !searchActive && selectedId) {
        const selected = byId.get(selectedId);
        visible = selected ? [selected, ...relatedTo(selected)] : visible;
    }
    const positions = layout(visible);
    nodesContainer.replaceChildren();
    lines.replaceChildren();
    graph.style.setProperty('--graph-zoom', zoom);
    document.getElementById('graph-empty').hidden = !searchActive || visible.length > 0;
    result.textContent = `${visible.length} élément${visible.length > 1 ? 's' : ''} affiché${visible.length > 1 ? 's' : ''}`;

    const root = document.createElement('button');
    root.className = 'graph-node graph-root';
    root.textContent = 'rec117';
    root.title = carteOuverte
        ? (navigation.length ? 'Revenir à l’étape précédente' : 'Fermer la carte mentale')
        : 'Ouvrir la carte mentale';
    root.style.left = '50%';
    root.style.top = '50%';
    root.addEventListener('click', () => {
        if (!carteOuverte) {
            carteOuverte = true;
            selectedId = null;
            navigation.length = 0;
            detailsTitle.textContent = 'Carte mentale ouverte';
            detailsDescription.textContent = 'Choisissez une catégorie pour commencer.';
            detailsRelations.replaceChildren();
        } else if (navigation.length) {
            showDetails(byId.get(navigation.pop()), false);
            return;
        } else if (selectedId) {
            selectedId = null;
            detailsTitle.textContent = 'Carte mentale ouverte';
            detailsDescription.textContent = 'Choisissez une catégorie pour continuer.';
            detailsRelations.replaceChildren();
        } else {
            carteOuverte = false;
            selectedId = null;
            detailsTitle.textContent = 'Carte mentale fermée';
            detailsDescription.textContent = 'Cliquez sur rec117 pour ouvrir la carte.';
            detailsRelations.replaceChildren();
        }
        render();
    });
    nodesContainer.appendChild(root);

    const coordinates = new Map([['root', { x: 50, y: 50 }]]);
    visible.forEach(node => {
        const position = positions.get(node.id);
        coordinates.set(node.id, position);
        const element = document.createElement('button');
        element.className = `graph-node graph-${node.type}${selectedId === node.id ? ' selected' : ''}`;
        element.textContent = node.label;
        element.title = `${typeNames[node.type]} : ${node.label}`;
        element.style.left = `${position.x}%`;
        element.style.top = `${position.y}%`;
        if (node.fiche) {
            element.dataset.fiche = node.fiche;
        }
        element.addEventListener('click', () => showDetails(node));
        nodesContainer.appendChild(element);
    });

    visible.forEach(node => relatedTo(node).filter(relation => coordinates.has(relation.id)).forEach(relation => {
        const from = coordinates.get(node.id);
        const to = coordinates.get(relation.id);
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', `${from.x}%`);
        line.setAttribute('y1', `${from.y}%`);
        line.setAttribute('x2', `${to.x}%`);
        line.setAttribute('y2', `${to.y}%`);
        line.classList.toggle('highlight', selectedId === node.id || selectedId === relation.id);
        lines.appendChild(line);
    }));
    visible.filter(node => ['artiste', 'lieu', 'genre', 'question'].includes(node.type)).forEach(node => {
        const position = coordinates.get(node.id);
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', '50%');
        line.setAttribute('y1', '50%');
        line.setAttribute('x2', `${position.x}%`);
        line.setAttribute('y2', `${position.y}%`);
        line.classList.toggle('highlight', selectedId === node.id);
        lines.prepend(line);
    });
}

document.querySelectorAll('.type-filter').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.type-filter').forEach(item => item.classList.remove('actif'));
    button.classList.add('actif');
    activeType = button.dataset.type;
    carteOuverte = true;
    navigation.length = 0;
    selectedId = null;
    render();
}));
[searchInput, dateFrom, dateTo].forEach(input => input.addEventListener('input', () => {
    carteOuverte = true;
    render();
}));
document.getElementById('mindmap-reset').addEventListener('click', () => {
    searchInput.value = '';
    dateFrom.value = '';
    dateTo.value = '';
    activeType = 'all';
    carteOuverte = true;
    selectedId = null;
    navigation.length = 0;
    document.querySelectorAll('.type-filter').forEach(item => item.classList.toggle('actif', item.dataset.type === 'all'));
    render();
});
document.getElementById('graph-zoom-in').addEventListener('click', () => { zoom = Math.min(1.35, zoom + .1); render(); });
document.getElementById('graph-zoom-out').addEventListener('click', () => { zoom = Math.max(.75, zoom - .1); render(); });
document.getElementById('graph-zoom-reset').addEventListener('click', () => { zoom = 1; render(); });
render();
