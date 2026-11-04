// === Page Carte Mentale ===
// L'arbre est déjà écrit par Django (mindmap.html). Un clic sur un élément ouvre ou ferme sa branche :
// la classe "ouvert" sur son <li> affiche la liste de ses enfants (voir mindmap.css).
// Les interviews et extraits ouvrent aussi leur fiche, grâce à data-fiche (voir modal.js).

document.querySelectorAll('.arbre .noeud').forEach(noeud => {
    noeud.addEventListener('click', () => noeud.parentElement.classList.toggle('ouvert'));
});
