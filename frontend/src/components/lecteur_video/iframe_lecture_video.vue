<script>

import ClientAPI from "@model/clientAPI";
import { videoStore } from "@model/videoStore";
import { nextTick } from 'vue';

export default {
  name: 'iframe_lecture_video',
  
  emits: ['lancement_prochaine_video'],

  props: {
    // Passer l'objet vidéo (Interview ou Extrait) en prop
    videoObject: {
      type: Object,
      required: false,
      default: null
    },
    // Type de vidéo : 'interview' ou 'extrait'
    videoType: {
      type: String,
      required: false,
      validator: (value) => ['interview', 'extrait'].includes(value)
    },
    // Seuil de progression pour marquer comme vu (par défaut 70%)
    progressThreshold: {
      type: Number,
      default: 70,
      validator: (value) => value > 0 && value <= 100
    },
    // L'extrait actuellement en lecture (pour les interviews)
    currentExtrait: {
      type: Object,
      required: false,
      default: null
    }
  },

  data() {
    return {
      player: null,
      user: ClientAPI.current_user, // peut être null si le user n'est pas connecté
      videoDuration: 0,
      maxProgressReached: 0, // Progression maximale atteinte (en secondes)
      hasMarkedAsWatched: false, // Pour éviter les appels multiples
      // Suivi de la progression de chaque extrait pour les interviews
      extraitsProgress: {}, // { uuid_extrait: { duration: X, maxProgress: Y, marked: boolean } }
      currentExtraitStartTime: 0 // Temps de début de l'extrait actuel dans l'interview
    };
  },

  methods: {
    /* Charge l'API YouTube si elle n'est pas déjà chargée */
    loadYouTubeAPI() {
      if (window.YT && window.YT.Player) return Promise.resolve(window.YT);

      if (!window._ytApiPromise) {
        window._ytApiPromise = new Promise((resolve) => {
          const tag = document.createElement("script");
          tag.src = "https://www.youtube.com/iframe_api";
          window.onYouTubeIframeAPIReady = () => resolve(window.YT);
          document.head.appendChild(tag);
        });
      }

      return window._ytApiPromise;
    },


    /* Extrait l'ID vidéo YouTube d'une URL donnée */
    get_YT_videoId(url) {
      try {
        const u = new URL(url);
        if (u.hostname === "youtu.be") return u.pathname.slice(1);
        if (u.hostname.includes("youtube.com")) {
          if (u.pathname.startsWith("/embed/")) return u.pathname.split("/")[2];
          if (u.searchParams.has("v")) return u.searchParams.get("v");
        }
      } catch {
        console.warn("URL YouTube invalide :", url);
      }
      return null;
    },

    /**
     * Calcule la durée totale de la vidéo et initialise le suivi des extraits
     * Pour un extrait : utilise extrait.duree
     * Pour une interview : additionne les durées de tous les extraits
     */
    async calculateTotalDuration() {
      if (!this.videoObject) return 0;

      try {
        if (this.videoType === 'extrait') {
          // Pour un extrait, utiliser directement sa durée
          return this.videoObject.duree || 0;
        } else if (this.videoType === 'interview') {
          // Pour une interview, initialiser le suivi de chaque extrait
          const extraits = await this.videoObject.extraits();
          if (!extraits || extraits.length === 0) {
            console.warn(`Aucun extrait trouvé pour l'interview ${this.videoObject.uuid}`);
            return 0;
          }
          
          let totalDuration = 0;
          let cumulativeTime = 0;
          
          // Initialiser le suivi de progression pour chaque extrait
          for (let extrait of extraits) {
            const duration = extrait.duree || 0;
            this.extraitsProgress[extrait.uuid] = {
              duration: duration,
              startTime: cumulativeTime,
              endTime: cumulativeTime + duration,
              maxProgress: 0,
              marked: false
            };
            totalDuration += duration;
            cumulativeTime += duration;
          }
          
          return totalDuration;
        }
      } catch (err) {
        console.error("Erreur lors du calcul de la durée totale:", err);
        return 0;
      }
      return 0;
    },

    /**
     * Trouve l'extrait actuellement lu en fonction du temps de l'interview
     */
    getCurrentExtraitFromTime(currentTime) {
      for (let uuid in this.extraitsProgress) {
        const extrait = this.extraitsProgress[uuid];
        if (currentTime >= extrait.startTime && currentTime < extrait.endTime) {
          return { uuid, ...extrait };
        }
      }
      return null;
    },

    startTracking() {
      videoStore.intervalId = setInterval(() => {
        if (this.player && typeof this.player.getCurrentTime === "function") {
          const currentTime = this.player.getCurrentTime();
          videoStore.currentTime = currentTime;
          this.checkProgress(currentTime);
        }
      }, 1000);
    },

    stopTracking() {
      if (videoStore.intervalId) {
        clearInterval(videoStore.intervalId);
        videoStore.intervalId = null;
      }
    },

    /**
     * Vérifie la progression et marque la vidéo comme vue si le seuil est atteint
     */
    checkProgress(currentTime) {
      // Ne rien faire si l'utilisateur n'est pas connecté
      if (!this.user || !this.videoObject || !this.videoType) {
        return;
      }

      if (this.videoType === 'interview') {
        // Pour une interview, suivre la progression de chaque extrait individuellement
        const currentExtrait = this.getCurrentExtraitFromTime(currentTime);
        
        if (currentExtrait) {
          // Calculer la progression dans l'extrait actuel
          const progressInExtrait = currentTime - currentExtrait.startTime;
          
          // Mettre à jour la progression maximale pour cet extrait
          if (progressInExtrait > this.extraitsProgress[currentExtrait.uuid].maxProgress) {
            this.extraitsProgress[currentExtrait.uuid].maxProgress = progressInExtrait;
          }
          
          // Vérifier si cet extrait a atteint 70%
          const progressPercentage = (this.extraitsProgress[currentExtrait.uuid].maxProgress / currentExtrait.duration) * 100;
          
          if (progressPercentage >= this.progressThreshold && !this.extraitsProgress[currentExtrait.uuid].marked) {
            this.markExtraitAsWatched(currentExtrait.uuid);
          }
        }
        
        // Mettre à jour la progression globale de l'interview
        if (currentTime > this.maxProgressReached) {
          this.maxProgressReached = currentTime;
        }
        
        // Vérifier si l'interview complète a atteint 70%
        if (this.videoDuration > 0 && !this.hasMarkedAsWatched) {
          const interviewProgressPercentage = (this.maxProgressReached / this.videoDuration) * 100;
          
          if (interviewProgressPercentage >= this.progressThreshold) {
            this.markInterviewAsWatched();
          }
        }
      } else {
        // Pour un extrait seul, comportement simple
        if (currentTime > this.maxProgressReached) {
          this.maxProgressReached = currentTime;
        }
        
        if (this.videoDuration > 0 && !this.hasMarkedAsWatched) {
          const progressPercentage = (this.maxProgressReached / this.videoDuration) * 100;
          
          if (progressPercentage >= this.progressThreshold) {
            this.markAsWatched();
          }
        }
      }
    },

    /**
     * Marque un extrait spécifique comme vu
     */
    async markExtraitAsWatched(extraitUuid) {
      if (!this.user || this.extraitsProgress[extraitUuid].marked) {
        return;
      }
      
      this.extraitsProgress[extraitUuid].marked = true;
      
      try {
        // Récupérer l'objet extrait
        const extraits = await this.videoObject.extraits();
        const extrait = extraits.find(e => e.uuid === extraitUuid);
        
        if (extrait) {
          await this.user.connect_extrait(extrait);
          console.log(`Extrait ${extraitUuid} marqué comme vu`);
        }
      } catch (error) {
        console.error(`Erreur lors du marquage de l'extrait ${extraitUuid}:`, error);
        this.extraitsProgress[extraitUuid].marked = false;
      }
    },

    /**
     * Marque l'interview comme vue
     */
    async markInterviewAsWatched() {
      if (this.hasMarkedAsWatched || !this.user) {
        return;
      }
      
      this.hasMarkedAsWatched = true;
      
      try {
        await this.user.connect_interview(this.videoObject);
        const interviewProgress = Math.round((this.maxProgressReached / this.videoDuration) * 100);
        console.log(`Interview ${this.videoObject.uuid} marquée comme vue (${interviewProgress}%)`);
      } catch (error) {
        console.error('Erreur lors du marquage de l\'interview:', error);
        this.hasMarkedAsWatched = false;
      }
    },

    /**
     * Marque la vidéo comme vue en créant le lien dans la BD (pour les extraits seuls)
     */
    async markAsWatched() {
      if (this.hasMarkedAsWatched || !this.user || !this.videoObject) {
        return;
      }

      this.hasMarkedAsWatched = true;

      try {
        await this.user.connect_extrait(this.videoObject);
        console.log(`Extrait ${this.videoObject.uuid} marqué comme vu`);
      } catch (error) {
        console.error('Erreur lors du marquage de la vidéo comme vue:', error);
        this.hasMarkedAsWatched = false;
      }
    },

    reset_old_lecteur() {
      if (this.player) {
        if (typeof this.player.destroy === 'function') {
          this.player.destroy();
        }
        this.player = null;
      }
      // Réinitialiser les données de progression
      this.videoDuration = 0;
      this.maxProgressReached = 0;
      this.hasMarkedAsWatched = false;
      this.extraitsProgress = {};
      this.currentExtraitStartTime = 0;
    },

    async initYouTube(videoId) {
      this.reset_old_lecteur();
      const YT = await this.loadYouTubeAPI();
      await nextTick();
      
      // Calculer la durée totale basée sur le type de vidéo
      this.videoDuration = await this.calculateTotalDuration();
      
      this.player = new YT.Player("player", {
        videoId,
        events: {
          onReady: (event) => {
            // Pour YouTube, on peut aussi récupérer la durée du player
            // mais on privilégie la durée calculée pour les interviews
            if (!this.videoDuration) {
              this.videoDuration = event.target.getDuration();
            }
            
            if (videoStore.currentTime) {
              event.target.seekTo(videoStore.currentTime);
            }
            if (videoStore.isPlaying) event.target.playVideo();
            else event.target.pauseVideo();
          },
          onStateChange: (event) => {
            if (event.data === YT.PlayerState.PLAYING) {
              videoStore.isPlaying = true;
              this.startTracking();
            }
            if (event.data === YT.PlayerState.PAUSED) {
              videoStore.isPlaying = false;
              this.stopTracking();
            }
            if (event.data === YT.PlayerState.ENDED) {
              // Marquer comme vu si la vidéo est terminée
              if (this.videoType === 'interview' && !this.hasMarkedAsWatched) {
                this.markInterviewAsWatched();
              } else if (this.videoType === 'extrait' && !this.hasMarkedAsWatched) {
                this.markAsWatched();
              }
              this.$emit('lancement_prochaine_video');
            }
          },
        },
      });
    },

    async initVimeo() {
      this.stopTracking();
      this.reset_old_lecteur();
      
      // Calculer la durée totale basée sur le type de vidéo
      this.videoDuration = await this.calculateTotalDuration();
      
      // Charger Vimeo API si pas encore là
      if (!window.Vimeo || !window.Vimeo.Player) {
        await new Promise((resolve) => {
          const script = document.createElement("script");
          script.src = "https://player.vimeo.com/api/player.js";
          script.onload = resolve;
          document.body.appendChild(script);
        });
      }

      // Créer l'iframe
      const container = document.getElementById("player");
      container.innerHTML = "";

      const iframe = document.createElement("iframe");
      iframe.src = videoStore.url;
      iframe.allow = "autoplay; fullscreen; picture-in-picture";
      iframe.allowFullscreen = true;
      iframe.style.width = "100%";
      iframe.style.height = "100%";
      container.appendChild(iframe);

      // Créer le player
      const vimeoPlayer = new window.Vimeo.Player(iframe);

      // Attendre qu'il soit prêt
      try {
        await vimeoPlayer.ready();
      } catch (e) {
        console.error("Vimeo jamais prêt :", e);
        return;
      }

      // Pour Vimeo, on peut aussi récupérer la durée du player
      // mais on privilégie la durée calculée pour les interviews
      if (!this.videoDuration) {
        try {
          this.videoDuration = await vimeoPlayer.getDuration();
        } catch (err) {
          console.warn("Impossible de récupérer la durée:", err);
        }
      }

      // Synchroniser l'état
      if (videoStore.currentTime) {
        try {
          await vimeoPlayer.setCurrentTime(videoStore.currentTime);
        } catch (err) {
          console.warn("Impossible de définir le temps :", err);
        }
      }

      if (videoStore.isPlaying) await vimeoPlayer.play();
      else await vimeoPlayer.pause();

      // Écoute des événements
      vimeoPlayer.on("timeupdate", ({ seconds }) => {
        videoStore.currentTime = seconds;
        this.checkProgress(seconds);
      });
      vimeoPlayer.on("play", () => (videoStore.isPlaying = true));
      vimeoPlayer.on("pause", () => (videoStore.isPlaying = false));
      vimeoPlayer.on("ended", () => {
        videoStore.currentTime = 0;
        // Marquer comme vu si la vidéo est terminée
        if (this.videoType === 'interview' && !this.hasMarkedAsWatched) {
          this.markInterviewAsWatched();
        } else if (this.videoType === 'extrait' && !this.hasMarkedAsWatched) {
          this.markAsWatched();
        }
        this.$emit('lancement_prochaine_video');
      });

      this.player = vimeoPlayer;
    },

    async update_player() {
      console.log("update")
      await nextTick();
      if (videoStore.url.includes("youtube") || videoStore.url.includes("youtu.be")) {
        const id = this.get_YT_videoId(videoStore.url);
        await this.initYouTube(id);
      } else {
        await this.initVimeo();
      }
    },

    set_url(lecteur) {
      videoStore.url = (lecteur === 'YouTube') ? videoStore.url_yt : videoStore.url_vimeo;
      this.update_player();
    }
  },

  async mounted() {
    console.log("test init iframe lecteru video")
    await nextTick();
    if (videoStore.url.includes("youtube")) {
      const id = this.get_YT_videoId(videoStore.url);
      await this.initYouTube(id);
    } else {
      await this.initVimeo();
    }
  },

  beforeUnmount() {
    if (this.player && this.player.destroy) this.player.destroy();
    this.stopTracking();
  }
};
</script>

<template>
  <div ref="rootElement" class="rootElement">
    <div class="player" id="player"></div>
  </div>
</template>

<style scoped>
.rootElement {
  width: 100%;
  height: 100%;
  background-color: #000;
}
</style>