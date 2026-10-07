<template>
  <div class="miniature-wrapper">
    <img v-if="url" :src="url" :alt="video.titre" />
    <p class="duree">{{ duree }}</p>
  </div>
</template>

<script>
import Model from '@model/model';

export default {
  name: 'miniature_video',
  props: ["video"],
  data() {
    return { 
      url: null,
      duree: "00:00",
      is_loading: false,
    };
  },
  methods: {
    async get_miniature(video, extraits) {
      try {
        // Cas 1 : c’est un extrait
        if (!extraits) {
          return (
            video.url_miniature_yt ||
            (await video.get_url_miniature_vimeo())
          );
        }

        // Cas 2 : c’est une interview
        if (!extraits || extraits.length === 0) {
          console.warn(`Aucun extrait trouvé pour l’interview ${video.uuid}`);
          return null;
        }
        const firstExtrait = extraits[0];
        return (
          firstExtrait.url_miniature_yt ||
          (await firstExtrait.get_url_miniature_vimeo())
        );
      } catch (err) {
        console.error("Erreur lors de la récupération de la miniature :", err);
        return null;
      }
    },

    async get_duree(video, extraits) {
      let time = 0;
      try {
        if (extraits) {
          // Si c’est une interview
          time = this.video.get_duree(extraits);
        } else {
          // Si c’est un extrait
          time = video.duree;
        }
      } catch (err) {
        console.error("Erreur dans get_duree :", err);
      }
      return Model.format_duree(time);
    },

    async update_miniature(){
      let extraits;
      if (this.video.extraits){
        extraits = await this.video.extraits()
        this.url = await this.get_miniature(this.video, extraits);
        this.duree = await this.get_duree(this.video, extraits);
        this.is_loading = false;
      }
      else {
        this.url = await this.get_miniature(this.video, null);
        this.duree = await this.get_duree(this.video, null);
        this.is_loading = false;
      }
    }
  },


  watch: {
    video: {
      handler() {
        this.update_miniature();
      },
      immediate: true 
    }
  }


};
</script>

<style scoped>
.miniature-wrapper {
  position: relative;
  display: inline-block;
  width: 50%;
}

.miniature-wrapper img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 11px;
  object-fit: cover;
  background-color: var(--gris-moyen);
}

/* Le temps en bas à gauche de l’image */
.duree {
  position: absolute;
  bottom: -5px;
  right: 8px;
  color: white;
  font-size: 0.8rem;
  background: rgba(0, 0, 0, 0.6);
  padding: 2px 6px;
  border-radius: 4px;
}
</style>

