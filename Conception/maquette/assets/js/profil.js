// === Page Profil ===
// Les tables (UTILISATEUR, PLAYLIST, PLAYLIST_EXTRAIT...) et les fonctions d'accès viennent de data.js,
// les fonctions d'affichage (creerElement, formaterTimecode...) de utils.js

// === Identité de l'utilisateur ===
document.getElementById('profil-avatar').textContent = UTILISATEUR.nom_utilisateur.charAt(0).toUpperCase();
document.getElementById('profil-nom').textContent = UTILISATEUR.nom_utilisateur;
document.getElementById('profil-email').textContent = UTILISATEUR.email;

// === Préférences ===
const choixLecteur = document.getElementById('lecteur-prefere');
const confirmation = document.getElementById('lecteur-confirmation');

choixLecteur.value = UTILISATEUR.lecteur_prefere;

// Dans le site final, ce changement sera envoyé à l'API ; ici il n'est pas conservé
choixLecteur.addEventListener('change', () => {
    UTILISATEUR.lecteur_prefere = choixLecteur.value;
    const nomLecteur = choixLecteur.options[choixLecteur.selectedIndex].textContent;
    confirmation.textContent = `✓ ${nomLecteur} sera utilisé par défaut.`;
});

// === Playlists ===
// Durée d'un extrait en secondes (null si le timecode de fin n'est pas renseigné)
function dureeExtrait(extrait) {
    return extrait.timecode_fin === null ? null : extrait.timecode_fin - extrait.timecode_debut;
}

// Une ligne de playlist : un lien vers l'extrait, ouvert sur la page d'accueil
function creerLigneExtrait(extrait, position) {
    const artiste = artisteDeInterview(interviewDeExtrait(extrait));
    const duree = dureeExtrait(extrait);

    const miniature = creerElement('img', 'playlist-miniature');
    miniature.src = imageExtrait(extrait, 160, 90);
    miniature.alt = 'Miniature';

    const details = creerElement('span', 'playlist-extrait-details');
    details.append(...genresDeArtiste(artiste).map(creerPastille), ` ${artiste.nom_artiste}`);

    const textes = creerElement('span', 'playlist-extrait-textes');
    textes.append(creerElement('span', 'playlist-extrait-titre', extrait.titre_extrait), details);

    const lien = creerElement('a', 'playlist-extrait');
    lien.href = `index.html#extrait-${extrait.id_extrait}`;
    lien.append(
        creerElement('span', 'playlist-position', String(position)),
        miniature,
        textes,
        creerElement('span', 'playlist-duree', duree === null ? '—' : formaterTimecode(duree))
    );

    const ligne = creerElement('li');
    ligne.appendChild(lien);
    return ligne;
}

function creerPlaylist(playlist) {
    const extraits = extraitsDePlaylist(playlist);
    const dureeTotale = extraits.reduce((total, extrait) => total + (dureeExtrait(extrait) || 0), 0);

    const liste = creerElement('ol', 'playlist-extraits');
    extraits.forEach((extrait, index) => liste.appendChild(creerLigneExtrait(extrait, index + 1)));

    const bloc = creerElement('article', 'playlist');
    bloc.append(
        creerElement('h3', 'playlist-titre', playlist.titre_playlist),
        creerElement(
            'p',
            'playlist-infos',
            `Créée le ${formaterDate(playlist.date_creation)} • ${extraits.length} extraits • ${formaterTimecode(dureeTotale)}`
        ),
        liste
    );
    return bloc;
}

const playlists = playlistsDeUtilisateur(UTILISATEUR);
const conteneurPlaylists = document.getElementById('playlists');

if (playlists.length) {
    conteneurPlaylists.replaceChildren(...playlists.map(creerPlaylist));
} else {
    conteneurPlaylists.replaceChildren(creerElement('p', 'playlist-infos', "Vous n'avez pas encore de playlist."));
}
