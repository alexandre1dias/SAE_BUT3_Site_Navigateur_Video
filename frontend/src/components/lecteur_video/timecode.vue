<script>
import { toRaw, markRaw } from "vue";
import { videoStore } from "@model/videoStore";


export default {
  emits: ["toggle_aside", "redirect_extrait"],
  props: {
    interview: {type: Object,},
    liste_extraits: {type: Array,},
    


  },

  data() {
    return {
        dico_timecode : {},
    };

  },

  methods : {
    // Covertir durrée en heures:minutes:secondes (actuellment un int en secondes)
    format_duree(duree_seconds) {
        const hours = Math.floor(duree_seconds / 3600);
        const minutes = Math.floor((duree_seconds % 3600) / 60);
        const seconds = duree_seconds % 60;

        let formatted_hours = hours > 0 ? String(hours).padStart(2, '0') + ':' : '';
        let formatted_minutes = String(minutes).padStart(2, '0') + ':';
        let formatted_seconds = String(seconds).padStart(2, '0');

        // si pas d'heures, ne pas afficher les heures
        formatted_hours = hours > 0 ? formatted_hours : '';
        // si pas de minutes, afficher 00:
        formatted_minutes = (hours > 0 || minutes > 0) ? formatted_minutes : '00:';
        // si pas de secondes, afficher 00
        formatted_seconds = (hours > 0 || minutes > 0 || seconds > 0) ? formatted_seconds : '00';
        // Retourner la chaîne formatée
        let duree = formatted_hours + formatted_minutes + formatted_seconds;
        // console.log("duree: ", duree);
        return duree;
    },

    set_dico_timecode() {
        let current_time = 0;
        // console.log("liste_extraits dans set_dico_timecode: ", this.liste_extraits);
        for (let extrait of this.liste_extraits) {
            this.dico_timecode[extrait.titre] = this.format_duree(current_time);
            current_time += extrait.duree;
        }
        this.dico_timecode["duree"] = this.format_duree(current_time);
    },

    async onClick(extrait) {
      // met à jour le temps courant du videoStore
      clearInterval(videoStore.intervalId);
      videoStore.currentTime = 0;
      // émet l'événement pour rediriger vers l'extrait cliqué
      this.$emit('redirect_extrait', extrait);
    }



  },

  async mounted() {
      // console.log("les extraoit")
      console.log("liste extrait ", this.liste_extraits)

      this.set_dico_timecode();
      // console.log("dico_timecode dans timecode.vue: ", markRaw(this.dico_timecode));
  },






};

</script>

<template>
<div>
    <header>
        
        <h2>{{ interview.titre }}</h2>
        <img src="/imgs/close2.svg" alt="close" @click="this.$emit('toggle_aside')">
    </header>
    <p>Duree de l'interview : {{ this.dico_timecode["duree"] }}</p>
        
        <ul>
          <li v-for="extrait in liste_extraits" @click="onClick(extrait)">
            <span>{{ dico_timecode[extrait.titre] }}</span>&nbsp;{{ extrait.titre }}
          </li>

        </ul>

</div>


</template>

<style scoped>
div {
    background-color: var(--vert-pale);
    padding-left: 3%;
    padding-top: 1%;
    height:30%;
    overflow-y: auto;
    border-bottom: 3px solid var(--gris-taupe);
    
}
ul {
    list-style-type: none;
    padding-left: 3%;
    margin: 0;
    padding-bottom: 0;
    padding-bottom: 1%;
    max-height: 100%;
    
    
}

span {

    color: var(--bleu);
}

li {
    cursor: pointer;
    margin-bottom: 1%;
}   
p {
    margin: 0;
}

header {
  display: flex;
}

h2 {
  flex: 4;
  margin: 0;
}

img {
  width: 6%;
  height: 6%;
  cursor: pointer;
  margin-right: 2%;

}

</style>
