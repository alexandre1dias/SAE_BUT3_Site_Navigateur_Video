// === Page Profil ===
// La table UTILISATEUR vient de data.js

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
