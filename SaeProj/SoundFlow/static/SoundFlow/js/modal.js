// === Fenêtre modale d'une vidéo ===
// Partagée par la page d'accueil et la carte mentale.
// Toutes les fiches sont déjà écrites dans la page par Django (partials/fiche_*.html), cachées.
// Ce fichier affiche la bonne et lance la vidéo dans un lecteur YouTube ou Vimeo.

const modal = document.getElementById('video-modal');

// Arrête la vidéo en cours : on retire le lecteur et on remet la miniature
function arreterVideo() {
    modal.querySelectorAll('.lecteur-video').forEach(lecteur => lecteur.remove());
    modal.querySelectorAll('.en-lecture').forEach(entete => entete.classList.remove('en-lecture'));
}

// Affiche la fiche demandée, par exemple ouvrirFiche('extrait-3') affiche #fiche-extrait-3
function ouvrirFiche(nom) {
    arreterVideo();
    modal.querySelectorAll('.fiche').forEach(fiche => { fiche.hidden = true; });
    document.getElementById(`fiche-${nom}`).hidden = false;
    modal.querySelector('.modal-content').scrollTop = 0;
    modal.classList.add('active');
    document.body.classList.add('modal-ouverte');
}

function fermerModal() {
    arreterVideo();
    modal.classList.remove('active');
    document.body.classList.remove('modal-ouverte');
}

// Tout élément qui porte data-fiche ouvre la fiche correspondante au clic :
// cartes, bouton de l'interview à la une, bifurcations, éléments de la carte mentale
document.addEventListener('click', e => {
    const element = e.target.closest('[data-fiche]');
    if (element) ouvrirFiche(element.dataset.fiche);
});

// Transforme l'adresse d'une vidéo en adresse de lecteur intégrable dans la page
//   https://youtu.be/ID ou https://www.youtube.com/watch?v=ID  →  https://www.youtube.com/embed/ID
//   https://vimeo.com/ID                                       →  https://player.vimeo.com/video/ID
function adresseLecteur(lecteur, adresse, debut) {
    if (lecteur === 'youtube') {
        const id = adresse.includes('watch?v=')
            ? adresse.split('watch?v=')[1].split('&')[0]
            : adresse.split('/').pop().split('?')[0];
        return `https://www.youtube.com/embed/${id}?autoplay=1&start=${debut}`;
    }
    const id = adresse.split('/').pop().split('?')[0];
    return `https://player.vimeo.com/video/${id}?autoplay=1#t=${debut}s`;
}

// Bouton « Lancer la vidéo » : l'adresse et le départ sont dans ses attributs data-*.
// Le lecteur (une iframe YouTube ou Vimeo) remplace la miniature en haut de la fiche.
modal.querySelectorAll('.btn-lancer').forEach(bouton => {
    bouton.addEventListener('click', () => {
        const lecteur = bouton.parentElement.querySelector('.choix-lecteur').value; // 'youtube' ou 'vimeo'
        const adresse = bouton.dataset[lecteur];
        if (!adresse) {
            alert(`Pas de vidéo ${lecteur} pour cette fiche.`);
            return;
        }

        arreterVideo();
        const iframe = document.createElement('iframe');
        iframe.className = 'lecteur-video';
        iframe.src = adresseLecteur(lecteur, adresse, bouton.dataset.debut);
        iframe.allow = 'autoplay; fullscreen; picture-in-picture';
        iframe.allowFullscreen = true;
        // YouTube refuse de lire la vidéo si la page ne transmet pas son adresse (erreur 153)
        iframe.referrerPolicy = 'strict-origin-when-cross-origin';

        const entete = bouton.closest('.modal-header');
        entete.classList.add('en-lecture');
        entete.appendChild(iframe);
    });
});

document.getElementById('modal-close').addEventListener('click', fermerModal);

// Un clic sur le fond sombre ferme la modale
modal.addEventListener('click', e => {
    if (e.target === modal) fermerModal();
});