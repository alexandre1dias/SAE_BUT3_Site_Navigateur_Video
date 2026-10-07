<script>
import { markRaw } from 'vue';
import comp_baradmin from "@components/components_admin/nav_admin.vue";
import comp_extrait from '@components/components_admin/Admin_presentation_extrait.vue';
import comp_admin_trie_extrait from '@components/components_admin/Admin_trie.vue';

import Extrait from "@model/extrait.js";

export default {
  name: "page_admin_listextrait",
  components: {
    comp_baradmin,
    comp_extrait,
    comp_admin_trie_extrait,
  }, data() {
    return {
      extraits: null,
      search: [],
    };
  },

  methods: {

    searchExtrait($event) {
      this.search = $event;
    },
  },




  async mounted() {
    this.extraits = markRaw(await Extrait.list());
  },
}




</script>

<template>

  <comp_baradmin />

  <h1 class="text-center"> Question-Extrait </h1>

  <div class="row" style="margin-right:0;margin-left:0; padding-left: 10px; padding-right: 20px;">
    <comp_admin_trie_extrait :extraitsearch="search" @searchextrait=searchExtrait($event) />

    <div class="col-md-9 aggrandir">
      <ul class="scroller2  row" v-if="search.length === 0">
        <li class="row carte" v-for="extrait in this.extraits">
          <comp_extrait :current_extrait=extrait></comp_extrait>
        </li>
      </ul>

      <ul class="scroller2  row" v-else>
        <li class="row carte" v-for="extrait in this.search">
          <comp_extrait :current_extrait=extrait></comp_extrait>
        </li>
      </ul>

    </div>
  </div>



</template>

<style scoped>
.carte {
  padding: 5px;
  padding-bottom: 1em;
  transition: transform 0.3s ease, filter 0.3s ease;
}

.carte:hover {
  transform: translateY(-8px);
  cursor: pointer;
}

.card {
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir));
  transition: filter 0.3s ease;
}

.carte:hover .card {
  filter: drop-shadow(25px 18px 8px var(--noir));
}

li>.card {
  padding: 20px 50px 150px;
  margin: 10px 10px 10px 10px;
}

.scroller2 {
  width: 100%;
  height: 100vh;
  overflow-y: scroll;
  scrollbar-color: var(--blanc) #A6A6A6;
  scrollbar-width: thin;
  padding: 0;
  margin: 0;
  list-style-type: none;
  display: block;
}

.aggrandir {
  display: flex;
  flex-wrap: nowrap;
  list-style-type: none;
  flex-grow: 1;
  height: 80vh;
  overflow: hidden;
}
</style>
