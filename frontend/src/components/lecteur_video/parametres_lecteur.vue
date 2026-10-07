<script>
import { videoStore } from "@model/videoStore";

export default {

  data() {
    return {
      lecteurs: ["YouTube", "Viméo"],
      lecteur_selected: videoStore.lecteur
    }
  },

  methods : {
    set_lecteur(lecteur){
      /// console.log("lecteur", lecteur)
      this.$emit('set_lecteur', lecteur),
      this.lecteur_selected = lecteur
      /// console.log(videoStore.lecteur)
    }
  },

}
</script>

<template>
  <div 
    class="popup-parametres"
  >
    <ul class="popup-labels">
      <li v-for="lecteur in lecteurs" :key="lecteur" @click="set_lecteur(lecteur)">
        {{ lecteur }}
        <span v-if="lecteur === lecteur_selected">✅</span>
      </li>
    </ul>
  </div>
</template>


<style scoped>
.popup-parametres {
  position: absolute;
  background-color: var(--gris-foncer);
  color: var(--third-color);
  border: 2px solid var(--gris-taupe);
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  width: auto;
  height: auto;
  z-index: 10000;
}

.popup-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.popup-labels {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popup-labels li {
  margin-bottom: 0.5rem;
}
</style>
