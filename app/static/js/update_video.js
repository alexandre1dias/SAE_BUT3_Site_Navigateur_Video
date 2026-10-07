
document.addEventListener("DOMContentLoaded", function () {

    // Sélectionner les modales
    const addThemeModal = document.getElementById("addThemeModal");
    const addQuestionModal = new bootstrap.Modal(document.getElementById("addQuestionModal"));
    
    // Ajouter un événement lorsqu'on ferme la modale "addAuthorModal"
    addThemeModal.addEventListener("hidden.bs.modal", function () {
        // Rouvrir la modale "addInterviewModal"
        addQuestionModal.show();
    });
    
    // Sélectionner les modales
    const addStyleModal = document.getElementById("addStyleModal");
    const addArtistModal = new bootstrap.Modal(document.getElementById("addArtistModal"));
    
    // Ajouter un événement lorsqu'on ferme la modale "addAuthorModal"
    addDStyleModal.addEventListener("hidden.bs.modal", function () {
        // Rouvrir la modale "addInterviewModal"
        addArtistModal.show();
    });
    });
    