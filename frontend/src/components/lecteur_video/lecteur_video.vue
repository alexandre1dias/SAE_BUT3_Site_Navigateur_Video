<script>
import { markRaw } from 'vue';
import iframe_lecture_video from './iframe_lecture_video.vue';
import bar_liste_video from "./bar_liste_video.vue";
import timecode from "./timecode.vue";
import { videoStore } from "@model/videoStore";


export default {
  name: "page_lecteur_video",
  inject : ["extrait_current", "interview_current"],
  components: { iframe_lecture_video, bar_liste_video, timecode },

  data() {
    return {
      param_visible: false,
      pos_x_iframe: null,
      pos_y_iframe: null,
      aside_visible: true,
      interview: null,
      extrait: null,
      liste_extraits: null,
      base_url_yt: "https://www.youtube.com/embed/",
      base_url_vimeo: "https://player.vimeo.com/video/",
      url_yt: "",
      url_vimeo: "",
      url: null,
    };
  },

  computed: {
    // Détermine le type de vidéo à suivre
    videoType() {
      // Si on a une interview, on suit l'interview complète
      if (this.interview) {
        return 'interview';
      }
      // Sinon on suit juste l'extrait
      return 'extrait';
    },
    
    // Retourne l'objet vidéo à suivre
    videoObjectToTrack() {
      // Si on a une interview, c'est elle qu'on veut marquer comme vue
      if (this.interview) {
        return this.interview;
      }
      // Sinon on marque l'extrait seul comme vu
      return this.extrait;
    }
  },

  async mounted() {
    await this.update();
    if (this.$refs.iframe) {
      videoStore.iframeComponent = this.$refs.iframe;
    }
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.updatePopupPosition);
  },

  methods: {
    async update(){
      const interviewData = await this.interview_current.get();
      const extraitData = await this.extrait_current.get();
      
      if (interviewData) {
        this.interview = markRaw(interviewData);
      } else {
        this.interview = null;
      }

      if (extraitData) {
        // Ne pas utiliser markRaw pour extrait car on veut qu'il soit réactif
        this.extrait = extraitData;
        console.log("extrait", this.extrait);
      } else {
        this.extrait = null;
      }

      if (this.interview != null){ 
        this.liste_extraits = markRaw(await this.interview.extraits({'order' : 'APPARTIENT_A|position'}));
        console.log("liste des extraits", this.liste_extraits)
        if (!this.extrait){
          this.extrait = this.liste_extraits[0];
          this.extrait_current.set(this.liste_extraits[0]);
        }
      }
      else {
        this.liste_extraits = null;
      }

      if (this.extrait) {
        this.url_yt = this.base_url_yt + this.extrait.youtube_url;
        this.url_vimeo = this.base_url_vimeo + this.extrait.vimeo_url;
        this.redirect_extrait(this.extrait);
      }
    },

    picture_in_picture() {
      videoStore.isPictureInPicture = true;
      console.log("iframe", videoStore.iframeComponent)
      videoStore.iframeComponent.set_url(videoStore.lecteur);
      this.$router.push("/");
    },

    toggle_aside() {
      this.aside_visible = !this.aside_visible;
    },

    async redirect_extrait(extrait){
        // Mettre à jour l'extrait - Ne pas utiliser markRaw pour garder la réactivité
        this.extrait_current.set(extrait);
        this.extrait = extrait;

        // Mettre à jour les URLs
        this.url_yt = this.base_url_yt + this.extrait.youtube_url;
        this.url_vimeo = this.base_url_vimeo + this.extrait.vimeo_url;
        
        // Réinitialiser le store
        videoStore.isPlaying = true;

        // update videoStore
        videoStore.uuid = this.extrait.uuid;
        videoStore.url_yt = this.url_yt;
        videoStore.url_vimeo = this.url_vimeo;
        videoStore.url = (videoStore.lecteur === 'YouTube') ? videoStore.url_yt : videoStore.url_vimeo;
        this.url = videoStore.url;

        // update le player si il est présent
        if (!this.$refs.iframe) {
          console.error("iframe non trouvé, impossible de mettre à jour le player");
          return;
        }
        else{
          console.log("update player avec extrait:", this.extrait.titre);
          await this.$refs.iframe.update_player();
        }
    },

    async lancement_prochaine_video() {
      if (!this.interview) {
        return;
      }
      
      let index = this.liste_extraits.find(extrait => extrait.uuid === this.extrait.uuid).position;

      console.log("index", index)
      console.log("nb extraits", this.liste_extraits.length - 1)
      
      if (index < this.liste_extraits.length - 1) {
        let next_extrait = this.liste_extraits[index + 1];
        videoStore.currentTime = 0;
        await this.redirect_extrait(next_extrait);
      } else {
        console.log("Fin de la liste des extraits de l'interview");
      }
    },
  },
};
</script>

<template>
  <div class="layout">
    <main>
      <iframe_lecture_video
        v-if="url"
        :url="url"
        ref="iframe"
        :videoObject="videoObjectToTrack"
        :videoType="videoType"
        :progressThreshold="70"
        @lancement_prochaine_video="lancement_prochaine_video"
      />

      <div v-else class="player"></div>
      
      <div>
        <div id="bottom-iframe">
          <h2>{{ extrait?.titre || 'titre' }}</h2>
          <div class="right-content">
            <img src="/imgs/reduire.svg" alt="picture in picture" @click="picture_in_picture">
          </div>
        </div>

        <div id="description">
          <p>{{ extrait?.description || 'description vidéo' }}</p>
        </div>
      </div>
    </main>

    <aside v-show="aside_visible">
      <timecode
        v-if="liste_extraits && interview"
        :interview="interview"
        :liste_extraits="liste_extraits"
        @redirect_extrait="redirect_extrait"
        @toggle_aside="toggle_aside"
      />

      <bar_liste_video 
        @toggle_aside="toggle_aside" 
        @update="update"
        :liste_extraits_current_interview="liste_extraits"
      />
    </aside>
    <h2 v-show="!aside_visible" @click="toggle_aside"> < </h2>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  width: 100vw;
  height: 100vh;
}

main {
  flex: 5;
  background-color: var(--noir);
  padding: 1rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  margin: 0 auto;
  width: 83%;
  height: 100%;
  padding-left: 2%;
  padding-right: 2%;
}

#bottom-iframe {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 0.5rem;
  box-sizing: border-box;
  margin-top: 2%;
}

#bottom-iframe h2 {
  margin: 0;
}

#bottom-iframe .right-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

#bottom-iframe img {
  width: 2em;
  height: 2em;
  cursor: pointer;
}

#bottom-iframe a {
  color: var(--vert-neon);
  text-decoration: underline;
  cursor: pointer;
}

#description {
  margin-top: 2%;
  background-color: var(--gris-foncer);
  border: var(--gris-foncer);
  border-radius: 20px;
  padding: 1rem;
  box-sizing: border-box;
}

.layout aside{
  flex: 2.2;
  background-color: var(--gris-moyen);
  border-left: 3px solid var(--gris-taupe);
  display: flex;
  flex-direction: column;
}

.layout h2{
  margin-right: 10px;
  color: var(--vert-neon);
}

iframe{
  width: 100%;
  height: 100%;
}
</style>