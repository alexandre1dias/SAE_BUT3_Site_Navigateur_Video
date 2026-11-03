// === Fenêtre modale d'une vidéo ===
// Partagée par la page d'accueil et la carte mentale.
// Toutes les fiches sont déjà écrites dans la page par Django (partials/fiche_*.html), cachées.
// Ce fichier se contente d'afficher la bonne.

const modal = document.getElementById('video-modal');

// Affiche la fiche demandée, par exemple ouvrirFiche('extrait-3') affiche #fiche-extrait-3
function ouvrirFiche(nom) {
    modal.querySelectorAll('.fiche').forEach(fiche => { fiche.hidden = true; });
    document.getElementById(`fiche-${nom}`).hidden = false;
    modal.querySelector('.modal-content').scrollTop = 0;
    modal.classList.add('active');
    document.body.classList.add('modal-ouverte');
}

function fermerModal() {
    modal.classList.remove('active');
    document.body.classList.remove('modal-ouverte');
}

// Tout élément qui porte data-fiche ouvre la fiche correspondante au clic :
// cartes, bouton de l'interview à la une, bifurcations, éléments de la carte mentale
document.addEventListener('click', e => {
    const element = e.target.closest('[data-fiche]');
    if (element) ouvrirFiche(element.dataset.fiche);
});

// Bouton « Lancer la vidéo » : l'adresse et le départ sont dans ses attributs data-*
modal.querySelectorAll('.btn-lancer').forEach(bouton => {
    bouton.addEventListener('click', () => {
        const lecteur = bouton.parentElement.querySelector('.choix-lecteur').value; // 'youtube' ou 'vimeo'
        const adresse = bouton.dataset[lecteur] || 'aucune vidéo pour ce lecteur';
        const depart = bouton.dataset.debut !== '0' ? ` (à partir de ${bouton.dataset.debut} s)` : '';
        alert(`Lancement du lecteur ${lecteur} :\n${adresse}${depart}`);
    });
});

document.getElementById('modal-close').addEventListener('click', fermerModal);

// Un clic sur le fond sombre ferme la modale
modal.addEventListener('click', e => {
    if (e.target === modal) fermerModal();
});
