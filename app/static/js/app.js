import Graph from "graphology";
import Sigma from "sigma";
import forceAtlas2 from "graphology-layout-forceatlas2";
import { NodeImageProgram, NodePictogramProgram } from "@sigma/node-image";

import PNG_MIC from "../images/MicrophoneIcon.png";
import PNG_AMPOULE from "../images/ampoule.png";
import PNG_PLAYER from "../images/player.png";

let graphContainer;
let closeBtn;
let refreshBtn;
let legendContainer;

// Fonction pour appliquer un layout ForceAtlas2 avec des paramètres personnalisés
const applyForceAtlas2 = (graph) => {
  forceAtlas2.assign(graph, {
    iterations: 300,
    settings: {
      gravity: 0.05,
      scalingRatio: 3,
      strongGravityMode: false,
      adjustSizes: true,
    },
  });
};

// Fonction pour ajuster le graphe (centrer et redimensionner)
const resizeGraph = (sigmaInstance) => {
  sigmaInstance.refresh();
  const camera = sigmaInstance.getCamera();
  camera.animate(
    {
      ratio: 1.4,
    },
    {
      duration: 1000,
    }
  );
};

// Fonction pour activer l'interaction avec le graphe une fois chargé
const enableGraphInteraction = (sigmaInstance) => {
  graphContainer.setAttribute("data-status", "Cliquez pour explorer");
  graphContainer.classList.remove("text-hidden");

  // Ajout d'un événement pour agrandir
  graphContainer.addEventListener("click", () => {
    graphContainer.classList.add("expanded");
    document.body.classList.add("expanded");

    // Supprimer la classe `disabled` pour activer les interactions
    const sigmaContainer = document.getElementById("sigma-container");
    sigmaContainer.classList.remove("disabled");

    // Masquer le texte "Cliquez pour explorer"
    graphContainer.setAttribute("data-status", "");
    graphContainer.classList.add("text-hidden");
    resizeGraph(sigmaInstance);

    // Affichage de la légende en plein écran
    legendContainer.style.display = "block";
  });
};

// Fonction pour fermer la vue agrandie
const closeGraph = (event, sigmaInstance) => {
  event.stopPropagation(); // Empêche la propagation du clic vers le conteneur
  graphContainer.classList.remove("expanded");
  document.body.classList.remove("expanded");

  // Restaurer le texte d'exploration
  graphContainer.setAttribute("data-status", "Cliquez pour explorer");
  graphContainer.classList.remove("text-hidden");

  // Ajouter la classe `disabled` pour désactiver les interactions
  const sigmaContainer = document.getElementById("sigma-container");
  sigmaContainer.classList.add("disabled");

  resizeGraph(sigmaInstance);

  // Cacher la légende en quittant le plein écran
  legendContainer.style.display = "none";
};

// Fonction pour vider le graphe et le recharger
const refreshGraph = () => {
  fetch("/clear_graph_cache/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(), // Inclure le CSRF token
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        console.log("Cache vidé avec succès. Rechargement du graphe...");
        const container = document.getElementById("sigma-container");
        container.innerHTML = "";
        loadGraph();
      } else {
        console.error("Erreur lors de la suppression du cache :", data.message);
      }
    })
    .catch((error) => {
      console.error("Erreur de requête :", error);
    });
};

// Fonction pour récupérer le CSRF token depuis la balise <meta>
function getCSRFToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

function loadGraph() {
  // Chargement des données de graphe depuis l'API
  fetch("/get_graph_data")
    .then((response) => response.json())
    .then((data) => {
      const graph = new Graph();

      // Ajout des nœuds
      data.nodes.forEach((node) => {
        graph.addNode(node.id, {
          label: node.label,
          category: node.type, // Type ajouté pour clustering
          x: Math.random(),
          y: Math.random(),
          size:
            node.type === "Interview" ? 25 : node.type === "Artist" ? 40 : 15,
          color:
            node.type === "Interview"
              ? "#ff6f61"
              : node.type === "Artist"
              ? "#6abf69"
              : node.type === "Theme"
              ? "#4c91ff"
              : "#e3a3fb",
          borderColor: "#FFFFFF",
          type: "image",
          image:
            node.type === "Interview"
              ? PNG_PLAYER
              : node.type === "Artist"
              ? PNG_MIC
              : node.type === "Theme"
              ? PNG_AMPOULE
              : "",
        });
      });

      // Ajout des arêtes
      data.edges.forEach((edge) => {
        graph.addEdge(edge.source, edge.target, {
          label: edge.type,
          type: "arrow",
          color: "#cccccc",
          size: 1.5,
        });
      });

      // Appliquer la disposition ForceAtlas2 au début
      applyForceAtlas2(graph);

      const container = document.getElementById("sigma-container");
      container.classList.add("disabled");
      const sigmaInstance = new Sigma(graph, container, {
        renderEdgeLabels: false,
        defaultNodeLabelColor: "#333",
        defaultNodeLabelSize: 14,
        nodeProgramClasses: {
          image: NodeImageProgram,
          pictogram: NodePictogramProgram,
        },
      });

      // Ajuster automatiquement la vue
      resizeGraph(sigmaInstance);

      // Événement de clic sur les nœuds
      sigmaInstance.on("clickNode", function (e) {
        const nodeKey = e.node; // ID du nœud cliqué
        const nodeData = graph.getNodeAttributes(nodeKey); // Récupérer les attributs du nœud
        const nodeType = nodeData.category; // Supposons que le type est dans l'attribut "category"

        console.log(`Nœud cliqué : ${nodeKey} (${nodeType})`);

        let url;
        if (nodeType === "Artist") {
          url = `artist/${nodeKey}`; // URL pour les artistes
        } else if (nodeType === "Interview") {
          url = `interview/${nodeKey}/`; // URL pour les vidéos
        } else if (nodeType === "Theme") {
          url = `theme/${nodeKey}`; // URL pour les thèmes
        } else {
          console.error("Type de nœud non pris en charge :", nodeType);
          return;
        }

        // Rediriger vers la page correspondante
        window.location.href += url;
      });

      // Activer l'interaction une fois le graphe chargé
      enableGraphInteraction(sigmaInstance);
      console.log(graph);

      closeBtn.addEventListener("click", (event) =>
        closeGraph(event, sigmaInstance)
      );
    })
    .catch((error) => {
      console.error("Erreur de chargement des données du graphe", error);
      graphContainer.setAttribute("data-status", "Erreur de chargement.");
    });
}

document.addEventListener("DOMContentLoaded", () => {
  graphContainer = document.getElementById("graph-container");
  closeBtn = document.getElementById("close-btn");
  refreshBtn = document.getElementById("refresh-btn");

  legendContainer = document.getElementById("legend-container");

  refreshBtn.addEventListener("click", (event) => refreshGraph());
  loadGraph();
});
