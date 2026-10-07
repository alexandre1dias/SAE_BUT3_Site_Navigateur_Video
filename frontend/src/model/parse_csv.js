import ClientAPI from "@model/clientAPI.js";

/**
 * Parse un fichier CSV contenant des extraits d'interviews d'artistes
 * et crée les instances des Models correspondants
 * @param {File|string} file - Le fichier CSV ou son contenu
 * @returns {Promise<string>} job_id
 */
export async function parse(file) {
  const response = await ClientAPI.sendFile(ClientAPI.BASE_URL + "api/csv_import/", file);
  return response.job_id; // retourne le job_id pour pouvoir le poller
}

/**
 * Vérifie toutes les 2 secondes si le job CSV est terminé
 * Affiche un toast global quand le job est terminé
 * @param {string} jobId
 */
export async function pollCSVJob(jobId) {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(ClientAPI.BASE_URL + `api/csv_import/status/${jobId}/`);
      const data = await res.json();

      if (data.status === "success") {
        showGlobalToast(data.message, "success");
        clearInterval(interval);
      }
      if (data.status === "error") {
        showGlobalToast(data.message, "error");
        clearInterval(interval);
      }
    } catch (err) {
      console.error("Erreur lors du polling CSVJob:", err);
      clearInterval(interval);
    }
  }, 10000);
}

/**
 * Affiche un toast global
 */
export function showGlobalToast(message, type = "success") {
  localStorage.setItem(
    "globalToast",
    JSON.stringify({ message, type })
  );
  // Ici tu peux avoir un EventBus ou une logique Vue pour écouter ce localStorage et afficher la popup
}
