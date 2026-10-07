<script>
import { markRaw, toRaw } from 'vue';
import { videoStore } from "@model/videoStore";
import miniature_video from "@components/lecteur_video/miniature_video.vue";
import fetchRecommendations from '@model/recommandation';


// Todo ajouter gif de chargement pendant le fetch des vidéos

export default {
  components: { miniature_video, },
  emits: ["toggle_aside", 'update'],
  inject: ["extrait_current", "interview_current"],
  props: {
    liste_extraits_current_interview: {
      type: Object,

    }
  },
  data() {
    return {
      videos: null,
      selected: "",
      img_close: true,
      extrait: null,
      interview: null,
      page: 0,

    };
  },

  methods: {
    // À déplacer
    /* Récupère les vidéos recommandées en fonction de l'extrait ou de l'interview actuelle.
       Utilise un algorithme de recommandation basé sur des poids prédéfinis.
    */
    async current_reco() {
      if (this.selected != "reco") {
        this.page = 0
        this.selected = "reco";
        this.videos = []
      }
      this.videos = this.videos.concat(
        await fetchRecommendations(
          {
            video: this.extrait ? this.extrait.uuid :
              this.interview ? this.interview.uuid : null,
            chemin: videoStore.chemin,
            filters: null, page: this.page, size: 10
          }
        )
      );
      console.log('vidéo', this.videos);
    },



    /*
      * Récupère les interviews associées à l'extrait actuel.
      * Met à jour la liste des vidéos affichées avec ces interviews.
      */
    async interview_current_extrait() {
      this.selected = "playlists"
      this.videos = markRaw(await this.extrait.interviews())
    },


    /* Récupère les extraits associés à la question actuelle.
      * Met à jour la liste des vidéos affichées avec ces extraits.
      */
    async extraits_current_question() {
      if (this.selected != "questions") {
        this.page = 0
        this.selected = "questions"
        this.videos = []
      }
      const question = markRaw(await this.extrait.question);
      this.videos = this.videos.concat(
        await fetchRecommendations(
          {
            video: this.extrait ? this.extrait.uuid :
              this.interview ? this.interview.uuid : null,
            chemin: videoStore.chemin,
            filters: { 'Question': question.uuid },
            page: this.page, size: 10
          }
        )
      );
    },


    /* Récupère les extraits et interviews associés à l'artiste actuel.
      * Met à jour la liste des vidéos affichées avec ces extraits et interviews.
      */
    async extraits_interviews_current_artiste() {
      if (this.selected != "artiste") {
        this.page = 0
        this.selected = "artiste";
        this.videos = []
      }
      const artiste = markRaw(await this.extrait.artiste);
      this.videos = this.videos.concat(
        await fetchRecommendations(
          {
            video: this.extrait ? this.extrait.uuid :
              this.interview ? this.interview.uuid : null,
            chemin: videoStore.chemin,
            filters: { 'Artiste': artiste.uuid },
            page: this.page, size: 10
          }
        )
      );

    },


    /* Récupère les extraits associés au thème actuel.
      * Met à jour la liste des vidéos affichées avec ces extraits.
      */
    async extrait_current_theme() {
      if (this.selected != "thèmes") {
        this.page = 0
        this.selected = "thèmes"
        this.videos = []
      }
      const question = markRaw(await this.extrait.question);
      const theme = markRaw(await question.theme);
      this.videos = this.videos.concat(
        await fetchRecommendations(
          {
            video: this.extrait ? this.extrait.uuid :
              this.interview ? this.interview.uuid : null,
            chemin: videoStore.chemin,
            filters: { 'Thème': theme.uuid },
            page: this.page, size: 10
          }
        )
      );
    },



    /* Met à jour la liste vidéo en fonction de la vidéo sélectionnée.
      * Met à jour l'extrait ou l'interview actuelle selon le type de vidéo sélectionnée.
      * Réinitialise le store vidéo et émet un événement de mise à jour.
      */
    async update_liste_video(video) {
      console.log("update liste videp");
      // maj du extrait_current ou interview_current selon le type de video

      if (video.extraits) {
        // c'est une interview
        /// console.log(video)
        this.interview_current.set(video);


        ///console.log((await video.extraits)[0])
        this.extrait_current.set((await video.extraits())[0]);
      } else {
        // c'est un extrait
        this.extrait_current.set(video);
        this.interview_current.set(null);
      }
      // recupération des nouveau extrait et interview
      this.extrait = await this.extrait_current.get();
      this.interview = await this.interview_current.get();



      // reset du videoStore
      videoStore.isPlaying = true;
      clearInterval(videoStore.intervalId);
      videoStore.intervalId = null;
      videoStore.currentTime = 0;

      this.$emit('update');

      //update bar liste video
      this.selected = '';
      console.log("this.current_reco test")
      await this.current_reco()
      console.log("after update video reco", this.videos)

      this.$refs.miniature_videos.forEach(child => {
        child.update_miniature();
      });


    },


    /* Charge plus de vidéos en fonction de la catégorie sélectionnée.
      * Incrémente la page et appelle la méthode appropriée pour récupérer plus de vidéos.
      */
    async plus_video() {
      this.page++;
      switch (this.selected) {
        case 'reco': await this.current_reco(); break;
        case 'questions': await this.extraits_current_question(); break;
        case 'artiste': await this.extraits_interviews_current_artiste(); break;
        case 'thèmes': await this.extrait_current_theme(); break;
      }

    },

  },
  async mounted() {
    this.interview = toRaw(await this.interview_current.get());
    this.extrait = toRaw(await this.extrait_current.get());
    this.current_reco();
    if (this.interview) this.img_close = false;


  },

};

</script>

<template>
  <header>
    <nav class="header-nav">
      <ul class="menu">
        <li @click="current_reco" :class="{ selected: selected === 'reco' }">Recomendation</li>
        <!--si la video est un extrait-->
        <li v-if="this.interview === null" @click="extraits_interviews_current_artiste"
          :class="{ selected: selected === 'artiste' }">Artiste</li>
        <li v-if="this.interview === null" @click="extraits_current_question"
          :class="{ selected: selected === 'questions' }">Questions</li>
        <li v-if="this.interview === null" @click="extrait_current_theme" :class="{ selected: selected === 'thèmes' }">
          Thèmes</li>
        <li v-if="this.interview === null" @click="interview_current_extrait"
          :class="{ selected: selected === 'playlists' }">Playlists</li>

      </ul>

      <img v-if="img_close" src="/imgs/close.svg" alt="close" @click="this.$emit('toggle_aside')">
    </nav>

  </header>
  <main>
    <div>
      <div>
        <ul class="liste_video">
          <li v-for="(video) in videos" :key="video.uuid">
            <div>
              <miniature_video ref="miniature_videos" @click="update_liste_video(video)" :video="video" />
              <div class="video_text">
                <h4>{{ video.titre }}</h4>
                <p>{{ video.description }}</p>

              </div>
            </div>
          </li>
        </ul>
        <button @click="plus_video()">plus de video ...</button>
      </div>
    </div>
  </main>

</template>

<style scoped>
header,
main {
  background-color: var(--gris-foncer);
  padding: 0 0.5rem;
}

header {
  border-bottom: 1px solid var(--blanc);
  height: 5%;
  display: flex;
  align-items: center;
  /* centre verticalement */
}

main {
  height: 64%;
  /* 100-5(header)-30(timecode)-1 */
  flex-grow: 1;
  /* permet à main de prendre tout l'espace restant */
  overflow-y: auto;
  /* permet le scroll vertical */
}

.header-nav {
  width: 100%;
  display: flex;
  justify-content: space-between;
  /* menu à gauche, bouton X à droite */
  align-items: center;
  /* centre verticalement */

}

.header-nav>img {
  width: 6%;
  height: 6%;


  cursor: pointer;

}



.menu {
  display: flex;
  /* aligne les <li> horizontalement */
  list-style: none;
  /* supprime les puces */
  gap: 1rem;
  /* espace entre les items */
  margin: 0;
  padding: 0;
}

.menu li {
  cursor: pointer;
}

.selected {
  color: var(--vert-neon);
}



.close-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.search-bar {
  width: 100%;
  display: flex;
}

.search-bar input {
  width: 85%;
  height: 2rem;
  border: none;
  border-radius: 20px;
  padding-left: 2%;
  margin-right: 2%;
}



.liste_video {
  margin: 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  gap: 10px;
  flex-direction: column;
}

.liste_video li>div {
  list-style: none;
  display: flex;
}



.liste_video a {
  width: 55%;
  height: 55%;
  margin-right: 1em;
  margin-bottom: 2em;
}

.video_text {
  padding-right: 5%;
  flex-grow: 1;
}

p,
h4 {
  margin: 0;
}
</style>
