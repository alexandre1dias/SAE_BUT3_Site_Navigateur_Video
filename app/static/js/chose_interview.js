document.addEventListener("DOMContentLoaded", function () {
    // Sélectionner les modales
    const addAuthorModal = document.getElementById("addAuthorModal");
    const addInterviewModal = new bootstrap.Modal(document.getElementById("addInterviewModal"));

    // Ajouter un événement lorsqu'on ferme la modale "addAuthorModal"
    addAuthorModal.addEventListener("hidden.bs.modal", function () {
      // Rouvrir la modale "addInterviewModal"
      addInterviewModal.show();
    });
  });
