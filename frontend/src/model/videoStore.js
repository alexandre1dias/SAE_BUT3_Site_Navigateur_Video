// src/stores/videoStore.js
import { reactive } from "vue";

export const videoStore = reactive({
  uuid: "",
  url_yt: "",
  url_vimeo: "",
  url:"",
  lecteur: "YouTube",
  isPictureInPicture: false,
  currentTime: 0,   // <-- position actuelle en secondes
  isPlaying: true, // <-- statut lecture/pause
  intervalId: null,
  set_url: null,
  iframeComponent: null, // on stockera ici une instance du composant iframe
  chemin : [], // chemin de point d'entrer (list de mm_node ; do node.content?)
});
