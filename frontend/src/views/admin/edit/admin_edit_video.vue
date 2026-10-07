<script>
import { markRaw } from 'vue';
import comp_baradmin from "@components/components_admin/nav_admin.vue";

import popup_interview from "@components/components_admin/popup_admin_edit.vue";
import popup_creer_question from "@components/components_admin/popup_creer_question.vue";

import Extrait from "@model/extrait";

import Audio from "@model/audio";
import Question from "@model/question";
import Artiste from "@model/artiste";
import supprimer from "../supprimer.vue";
import tags from "../tags.vue"
import Tag from "@model/tag.js";

import edit_success from "../gestion/edit_success.vue"
import edit_error from '../gestion/edit_error.vue';

import { handleTagsConnected, handleTagsDisconnected, handleTagsCreated } from '../fn_save_tags.js';

export default {
  name: "page_admin_detail_video",



  components: {
    comp_baradmin,
    popup_interview,
    popup_creer_question,
    supprimer,
    tags,
    edit_success,
    edit_error

  }, data() {
    return {
      current_extrait: null,
      thumbnail: '/imgs/width551.png',
      laselectedAudio: "",    //Audio selectionner retourn null si rien     
      laselectedArtiste: "", //Artiste selectionner retourn null si rien
      laselectedQuestion: "",//Questio selectionner retourn null si rien 

      interviews: [],
      listeArtiste: [],    //liste des Artistes totals
      listeAudios: [],    //liste des Artistes totals

      listeQuestion: [],   //liste des Questions totals
      listetheme: [],   //liste des Questions totals
      popupDelete: false,
      searchValueTag: "",
      create: false,
      popup: false,
      popupSelectInterview: false, //Props pour popupSelectInterview
      popupCreerQuestion: false,
      popupSuccess: false,
      popupError: false,
      urlVimeoReconstruit: "",
      urlyoutubeReconstruit: "",

      reponse: null,

      tagsConnected: [],
      tagsToDisconnect: [],
      tagsToCreate: [],

      // Gestion des audios (liste pour un extrait)
      audioSelected: null,
      audioToConnect: [],  // Tableau d'audios à connecter
      audioToDisconnect: [],  // Tableau d'audios à déconnecter  
    };
  },




  methods: {

    handleTagsCreated(tags) {
      handleTagsCreated(this, tags)
    },

    handleTagsDisconnected(tags) {
      handleTagsDisconnected(this, tags)
    },

    handleTagsConnected(tag) {
      handleTagsConnected(this, tag)
    },



    async modificationDonnees() {
      if (this.create) {
        await this.enregistrer();
      } else {
        await this.Update();
      }
    },


    async validationExtrait() {
      let erreur = "";
      if (this.current_extrait.titre == null || this.current_extrait.titre == "") {
        erreur += "il manque un titre  \n";
      } if (this.current_extrait.question_uuid == null) {
        erreur += "il manque une question  \n";
      } if (this.current_extrait.youtube_url == "" && this.current_extrait.vimeo_url == "") {
        erreur += "il faut au moins un lien de video  \n";
      }
      return erreur;
    },


  async getYouTubeDuration(videoId) {
    // UTILISE LAPI YOUTUBE
    if (!videoId) {
      console.log("Pas de videoId fourni");
      return null;
    }

    try {
      const API_KEY = import.meta.env.YOUTUBE_API_KEY;
      
      if (!API_KEY) {
        console.error("Clé API YouTube manquante");
        return 1;
      }

      const response = await fetch(
        `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=contentDetails&key=${API_KEY}`
      );
      
      if (!response.ok) {
        console.log("Erreur API YouTube");
        return null;
      }
      
      const data = await response.json();
      
      if (data.items && data.items.length > 0) {
        const duration = data.items[0].contentDetails.duration;
        // Convertir ISO duration en secondes
        return this.parseDuration(duration);
      }
      
      return null;
    } catch (error) {
      console.error("Erreur lors de la récupération de la durée:", error);
      return null;
    }
  },

  // la fonction qui convertie la durée ISO en secondes
  parseDuration(duration) {
    const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
    if (!match) return 0;
    
    const hours = parseInt(match[1] || 0);
    const minutes = parseInt(match[2] || 0);
    const seconds = parseInt(match[3] || 0);
    
    return hours * 3600 + minutes * 60 + seconds;
  },


  async getVimeoDuration(videoId) {
      // Appel à l'API Vimeo
    if (!videoId) {
      console.log("Pas de videoId Vimeo fourni");
      return null;
    }

    try {
      const ACCESS_TOKEN = import.meta.env.VITE_VIMEO_ACCESS_TOKEN;
      
      if (!ACCESS_TOKEN) {
        console.error("Token d'accès Vimeo manquant");
        return 1;
      }

      const response = await fetch(
        `https://api.vimeo.com/videos/${videoId}`,
        {
          headers: {
            'Authorization': `Bearer ${ACCESS_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (!response.ok) {
        console.log("Erreur API Vimeo");
        return null;
      }
      
      const data = await response.json();
      
      //get la duree depuis l'API Vimeo
      if (data.duration) {
        return data.duration;
      }
      
      return null;
    } catch (error) {
      console.error("Erreur lors de la récupération de la durée Vimeo:", error);
      return null;
    }
  },



    async enregistrer() {

      try {
        //fonction pour enregistrer un extraits dans L'api
        this.message_error = await this.validationExtrait();

        if (this.message_error == "") {

          await this.current_extrait.create();
          //this.new_extrait = new markRaw(new Extrait({}));
          await this.save_relations();

          sessionStorage.setItem('popupSuccess', 'true');
          sessionStorage.setItem('create', this.create ? 'true' : 'false');

          // Reload brutal
          window.location.href = `/admin/extrait/${this.current_extrait.uuid}`;
        } else {
          this.popupError = true;
          setTimeout(() => {
            this.popupError = false;
          }, 5000)
        }


      } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error.toString());
        this.message_error = error.toString();
        this.popupError = true;
        setTimeout(() => {
          this.popupError = false;
        }, 5000)
      }

    },


    async Update() {
      try {
        this.current_extrait.duree = 0;

        this.message_error = await this.validationExtrait();

        if (this.message_error == "") {
          await this.current_extrait.update();
          await this.save_relations();

          sessionStorage.setItem('popupSuccess', 'true');
          sessionStorage.setItem('create', this.create ? 'true' : 'false');

          // Reload brutal
          window.location.href = `/admin/extrait/${this.current_extrait.uuid}`;
        } else {
          this.popupError = true;
          setTimeout(() => {
            this.popupError = false;
          }, 5000)
        }

      } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error.toString());
        this.message_error = error.toString();
        this.popupError = true;
        setTimeout(() => {
          this.popupError = false;
        }, 5000)
      }

    },



    async save_relations() {
      try {
        // Gérer les audios
        await this.save_audio();

        // Gérer les tags
        await this.save_tags_only();

      } catch (error) {
        console.error('Erreur lors de la sauvegarde des relations:', error);
        throw error;
      }
    },

    async save_audio() {
      try {
        console.log('save_audio appelé');
        console.log('audioToConnect:', this.audioToConnect);
        console.log('audioToDisconnect:', this.audioToDisconnect);

        // Connecter les audios dans le tableau
        for (const audio of this.audioToConnect) {
          console.log('Tentative de connexion audio:', audio);

          // Récupérer l'UUID et le nom depuis l'objet markRaw
          const audioUuid = audio.uuid;
          const audioName = audio.name;

          console.log('UUID:', audioUuid, 'Name:', audioName);

          // Créer un objet simple pour la connexion
          const simpleAudio = {
            uuid: audioUuid,
            name: audioName
          };

          console.log('Instance créée:', simpleAudio);

          await this.current_extrait.connect_audio(simpleAudio);
          console.log('Audio connecté avec succès:', audioName);
        }

        // Déconnecter les audios dans le tableau
        for (const audio of this.audioToDisconnect) {
          if (audio) {  // Vérifier que l'audio n'est pas null
            console.log('Tentative de déconnexion audio:', audio);

            const audioUuid = audio.uuid;
            const audioName = audio.name;

            const simpleAudio = {
              uuid: audioUuid,
              name: audioName
            };

            await this.current_extrait.disconnect_audio(simpleAudio);
            console.log('Audio déconnecté avec succès:', audioName);
          }
        }

        // Réinitialiser les tableaux audio
        this.audioToConnect = [];
        this.audioToDisconnect = [];
      } catch (error) {
        console.error('Erreur lors de la sauvegarde de l\'audio:', error);
        console.error('Détail de l\'erreur:', error.message);
        throw error;
      }
    },

    async save_tags_only() {
      try {
        // Connecter les tags existants
        for (const tag of this.tagsConnected) {
          await this.current_extrait.connect_tag(tag);
        }

        // Créer et connecter les nouveaux tags
        for (const tagData of this.tagsToCreate) {
          const newTag = await new Tag({ name: tagData.name }).create();
          await this.current_extrait.connect_tag(newTag);
        }

        // Déconnecter les tags
        for (const tag of this.tagsToDisconnect) {
          await this.current_extrait.disconnect_tag(tag);
        }

        // Réinitialiser les listes de tags
        this.tagsConnected = [];
        this.tagsToCreate = [];
        this.tagsToDisconnect = [];
      } catch (error) {
        console.error('Erreur lors de la sauvegarde des tags:', error);
        throw error;
      }
    },












    async creerNouveauArtiste() {

      if (this.laselectedArtiste != "" && this.laselectedArtiste != null) {
        if (!this.listeArtiste.find(a => a.name === this.laselectedArtiste)) {
          const newArtiste = new Artiste({});
          newArtiste.name = this.laselectedArtiste;
          await newArtiste.create()
          this.listeArtiste.push(newArtiste);
          this.current_extrait.artiste = await newArtiste.uuid;
          this.current_extrait.artiste_uuid = await newArtiste.uuid;

          alert('l\'artiste ' + newArtiste.name + ' est creer');
        } else {
          alert('l\'artiste existe deja')
        }
      } else {
        alert('pas de champs null pour artiste');
      }

    },


    async creerNouveauAudio() {

      if (this.laselectedAudio != "" && this.laselectedAudio != null) {
        if (!this.listeAudios.find(a => a.name === this.laselectedAudio)) {
          const newAudio = new Audio({});
          newAudio.name = this.laselectedAudio;
          await newAudio.create()
          this.listeAudios.push(newAudio);

          // Ajouter le nouvel audio au tableau des audios à connecter
          this.audioToConnect = [newAudio];
          this.audioToDisconnect = [];

          // Connecter l'audio à l'extrait via la relation audios
          if (this.current_extrait.uuid) {
            // Créer un objet simple pour éviter les problèmes markRaw
            const audioData = {
              uuid: newAudio.uuid,
              name: newAudio.name
            };
            await this.current_extrait.connect_audio(audioData);
          }

          alert('l\'audio ' + newAudio.name + ' est creer');
        } else {
          alert('l\'audio existe deja')
        }
      } else {
        alert('pas de champs null pour audio');
      }

    },

    creerNouvelleQuestion() {

      if (this.laselectedQuestion != "" && this.laselectedQuestion != null) {
        if (!this.listeQuestion.find(a => a.texte === this.laselectedQuestion)) {
          this.popupCreerQuestion = true;
          /*
          const newQuestion = new Question({});
          newQuestion.name = this.laselectedQuestion;
          newQuestion.create()
          this.listeQuestion.push(newQuestion);
          */

        } else {
          alert('question existe deja');
        }
      } else {
        this.popupCreerQuestion = true;
      }

    },








    popupchange() {
      this.popup = !this.popup;
    },

    popupchangequestion() {
      this.popupCreerQuestion = !this.popupCreerQuestion;
    },



    popupchangeInterview() {
      //permet de changer l'etat de la popup Interview
      this.popupSelectInterview = !this.popupSelectInterview

    },












    SelectedArtisteId() {
      //reccupere l'artiste de la liste en reccuperant le nom de l'artiste selectionner
      //reccupere l'artiste de la liste
      const artiste = this.listeArtiste.find(a => a.name === this.laselectedArtiste);



      //verifie si artiste existe et n'es pas null
      if (artiste) {
        this.current_extrait.artiste = artiste.uuid;
        this.current_extrait.artiste_uuid = artiste.uuid;
      } else {
        this.current_extrait.artiste = null;
        this.current_extrait.artiste_uuid = null;
      }

    },


    SelectedAudiosId() {
      //reccupere l'audio de la liste en reccuperant le nom de l'audio selectionner
      const audio = this.listeAudios.find(a => a.name === this.laselectedAudio);


      //verifie si audio existe et n'es pas null
      if (audio) {
        this.audioSelected = audio;

        // Vider et ajouter le nouvel audio à connecter
        this.audioToConnect = [audio];
        this.audioToDisconnect = [];

        console.log('Audio sélectionné pour connexion:', audio);
      } else {
        this.audioSelected = null;
        this.audioToConnect = [];
        // Si on déselectionne, on déconnecte tous les audios actuels
        this.audioToDisconnect = [this.audioSelected];
      }

      console.log('État audio - ToConnect:', this.audioToConnect, 'ToDisconnect:', this.audioToDisconnect);
    },

    FoncSelectedQuestion() {
      //reccupere la Question de la liste en reccuperant le text de la Question selectionner

      //reccupere l'question de la liste
      const question = this.listeQuestion.find(a => a.texte === this.laselectedQuestion);

      //verifie si question existe et n'es pas null
      if (question) {
        this.current_extrait.question = question.uuid;
        this.current_extrait.question_uuid = question.uuid;
      } else {
        this.current_extrait.question = null;
        this.current_extrait.question_uuid = null;
      }

    },

    async recupeArtiste() {
      //reccupere la liste des Artistes
      this.listeArtiste = markRaw(await Artiste.list());
    },


    async recupeAudio() {
      //reccupere la liste des Audios
      this.listeAudios = markRaw(await Audio.list());
    },

    async recupeQuestion() {
      //reccupere la liste des Questions
      this.listeQuestion = markRaw(await Question.list());
    },

















    async validateYouTubeVideo(url) {
      // Extraire l'ID YouTube
      if ((this.get_YT_videoId(url) == null || this.get_YT_videoId(url) == "") || !this.get_YT_videoId(url)) {
        console.log("URL YouTube invalide");
        return '/imgs/width551.png';
      }
      const videoId = this.get_YT_videoId(url);
      if (!videoId) {
        console.log("URL YouTube invalide");
        return '/imgs/width551.png';
      }
      try {
        const response = await fetch(
          `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`
        );

        if (!response.ok) {
          if (response.status === 404) {
            console.log("Vidéo introuvable");
          } else {
            console.log("Vidéo inaccessible");
          }
          return '/imgs/width551.png';
        }
        const data = await response.json();
        return data.thumbnail_url;

      } catch (error) {
        return '/imgs/width551.png';
      }
    },


    async validateVimeoVideo(url) {
      // Extraire l'ID Vimeo
      if (this.get_Vimeo_videoId(url) == null || this.get_Vimeo_videoId(url) == "" || !this.get_Vimeo_videoId(url)) {
        return '/imgs/width551.png';
      }
      const videoId = this.get_Vimeo_videoId(url);
      if (!videoId) {
        console.log("URL Vimeo invalide");
        return '/imgs/width551.png';
      }

      try {
        const response = await fetch(
          `https://vimeo.com/api/oembed.json?url=https://vimeo.com/${videoId}`
        );

        if (!response.ok) {
          if (response.status === 404) {
            console.log("Vidéo introuvable")
          } else {
            console.log("Vidéo inaccessible")
          }
          return '/imgs/width551.png'
        }

        const data = await response.json();
        return data.thumbnail_url;
      }
      catch (error) {
        return '/imgs/width551.png';
      }
    },

    async migniature_video() {

      if (this.urlVimeoReconstruit != null && !this.urlVimeoReconstruit.includes('https') && this.urlVimeoReconstruit != '') {
        this.urlVimeoReconstruit = 'https://vimeo.com/' + this.urlVimeoReconstruit;
      }

      if (this.urlyoutubeReconstruit != null && !this.urlyoutubeReconstruit.includes('https') && this.urlyoutubeReconstruit != '') {
        this.urlyoutubeReconstruit = 'https://www.youtube.com/watch?v=' + this.urlyoutubeReconstruit;
      }

      try {
        this.current_extrait.youtube_url = this.get_YT_videoId(this.urlyoutubeReconstruit);
      } catch {
        this.current_extrait.youtube_url = "";
        console.log('erreur');
      }

        try {
          // Récupérer la durée de la vidéo YouTube
          this.current_extrait.youtube_url = this.get_YT_videoId(this.urlyoutubeReconstruit);
          if (this.current_extrait.youtube_url) {
            const duration = await this.getYouTubeDuration(this.current_extrait.youtube_url);
            if (duration) {
              this.current_extrait.duree = duration;
            }
          }
        } catch {
          this.current_extrait.youtube_url = "";
          console.log('erreur');
        }

      try {
        this.current_extrait.vimeo_url = await this.get_Vimeo_videoId(this.urlVimeoReconstruit);
      } catch {
        this.current_extrait.vimeo_url = "";
        console.log('erreur');
      }


      let vimeoId = null;

      try {
        // Extraction de l'ID Vimeo
        vimeoId = await this.get_Vimeo_videoId(this.urlVimeoReconstruit);
        this.current_extrait.vimeo_url = vimeoId;
        
        //reccuperation de la duree de la video
        if (vimeoId) {
           this.current_extrait.duree = await this.getVimeoDuration(vimeoId);
        }
      } catch (error) {
        // En cas d'erreur
        this.current_extrait.vimeo_url = "";
        console.log('Erreur lors de l\'extraction de l\'ID Vimeo:', error);
      }


      if (this.current_extrait.url_miniature_yt != null && this.current_extrait.url_miniature_yt.includes(this.current_extrait.youtube_url) && !this.current_extrait.youtube_url == "") {
        this.thumbnail = await this.validateYouTubeVideo(this.urlyoutubeReconstruit);

      } else {
        this.thumbnail = await this.validateVimeoVideo(this.urlVimeoReconstruit);
      }
    },

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


    get_Vimeo_videoId(url) {
      try {
        const u = new URL(url);
        if (u.hostname.includes("vimeo.com")) {
          if (u.pathname.match(/^\/\d+$/)) {
            return u.pathname.slice(1);
          }
          const match = u.pathname.match(/\/(\d+)$/);
          if (match) return match[1];
          if (u.pathname.startsWith("/video/")) {
            return u.pathname.split("/")[2];
          }
        }
      } catch {
        console.warn("URL Vimeo invalide :", url);
      }
      return null;
    },


    async chargerSelection(field, displayProp) {
      if (await this.current_extrait[field] != null && await this.current_extrait[field] !== undefined) {
        const entity = markRaw(await this.current_extrait[field]);

        // Valeur affichée
        switch (field) {
          case "question":
            this.laselectedQuestion = await entity[displayProp];
            break;

          case "audio":
            this.laselectedAudio = await entity[displayProp];
            break;
          case "artiste":
            this.laselectedArtiste = await entity[displayProp];
            break;

        }



        // Remplacement par l'uuid
        this.current_extrait[field] = entity.uuid;
        this.current_extrait[field].uuid = entity.uuid;
      }
    },


  },











  async mounted() {

    // Popup succès après reload brutal
    if (sessionStorage.getItem('popupSuccess') === 'true') {
      this.popupSuccess = true;

      // Déterminer si c'était en mode création ou modification
      this.createMode = sessionStorage.getItem('create') === 'true';
      console.log("createmode", this.createMode)

      sessionStorage.removeItem('popupSuccess');
      sessionStorage.removeItem('create');

      // ⏱ cacher après 5 secondes
      setTimeout(() => {
        this.popupSuccess = false;
      }, 5000);
    }

    await this.recupeArtiste();
    await this.recupeQuestion();
    await this.recupeAudio();

    //reccuperation de l'id en parametre
    const ExtraitId = this.$route.params.id;
    if (ExtraitId != null) {
      //reccuperation de l'Extrait via l'id



      this.current_extrait = markRaw(await Extrait.detail(ExtraitId));
      this.interviews = markRaw(await this.current_extrait.interviews());
      this.tags = markRaw(await this.current_extrait.tags());

      console.log(this.current_extrait);

      try {
        this.current_extrait.audio = (await this.current_extrait.audios)
        console.log(this.current_extrait.audio);
      } catch (error) {
        console.log("pas de audio definie")
      }

      try {
        this.current_extrait.question_uuid = (await this.current_extrait.question).uuid
      } catch {
        console.log("pas de question definie")
      }

      await this.chargerSelection('question', 'texte');
      await this.chargerSelection('audio', 'name');
      await this.chargerSelection('artiste', 'name');

    } else {
      this.current_extrait = markRaw(await new Extrait({}));
      this.create = true;
    }
    this.urlVimeoReconstruit = this.current_extrait.vimeo_url;
    this.urlyoutubeReconstruit = this.current_extrait.youtube_url;
    this.migniature_video()


  }
};












































</script>

<template>
  <comp_baradmin />

  <form v-if="current_extrait" action="" class="row" style="--bs-gutter-x: 0em;">




    <div class="row" style="--bs-gutter-x: 0em;">

      <div class="col-md-4" style="text-decoration: none; color: inherit; padding: 1em;">
        <img :src="thumbnail" class="migniature" alt="migniature">
      </div>

      <div class="col-md-6 scroller basemodif" style="width: 65%; height: 100%; padding: 1em;">

        <div class="row" style="--bs-gutter-x: 0em;">
          <div class=" input-group mb-3">
            <span class="input-group-text colovert" id="basic-addon3"> Titre :</span>
            <input list="Questiondata" id="question" name="question" class="form-control"
              v-model="this.current_extrait.titre" />
          </div>
        </div>

        <div class="row" style="--bs-gutter-x: 0em;">
          <div class=" input-group mb-3">
            <span class="input-group-text colovert" id="basic-addon3"> Question :</span>

            <input list="Questiondata" id="question" name="question" class="form-control colovert"
              style="border: solid; border-color: var(--vert-midel);" v-model="laselectedQuestion"
              @input="FoncSelectedQuestion" />

            <datalist id="Questiondata">
              <option v-for="question in listeQuestion" :key="question.id" :value="question.texte"
                :label="question.texte"> </option>
            </datalist>



            <button class="bt" type="button" @click="creerNouvelleQuestion"
              style="background-color: var(--gris-ultraclair);"> <img src="/imgs/add_black.svg" alt="add" class="col ">
            </button>
          </div>
        </div>


        <div class="row" style="--bs-gutter-x: 0em;">
          <div class="input-group mb-3">
            <span class="input-group-text colovert">Artiste :</span>
            <input list="Artistedata" id="choixArtiste" name="choixArtiste" class="form-control colovert"
              style="border: solid; border-color: var(--vert-midel);" v-model="laselectedArtiste"
              @input="SelectedArtisteId">

            <datalist id="Artistedata">
              <option v-for="artiste in listeArtiste" :key="artiste.id" :value="artiste.name" :label="artiste.name">
              </option>
            </datalist>

            <button class="bt" type="button" @click="creerNouveauArtiste"
              style="background-color: var(--gris-ultraclair);"> <img src="/imgs/add_black.svg" alt="add" class="col  ">
            </button>
          </div>
        </div>

        <div class="row" style="--bs-gutter-x: 0em;">
          <div class="input-group mb-3 ">
            <span class="input-group-text colovert">
              <img class="col" src="/imgs/date.svg" style="padding-right: 10px; width: 1em; height: 1em;" alt="">
              Date :
            </span>
            <input class="col form-control" type="date" lang="fr" id="date" name="name4"
              style="background-color: var(--gris-ultraclair);" v-model="this.current_extrait.uploaded_at" />
          </div>
        </div>

        <div class="row" style="--bs-gutter-x: 0em;">
          <div class="input-group mb-3 ">
            <span class="input-group-text colovert" id="basic-addon1">youtube_url :</span>
            <input type="text" class="form-control textfield" id="youtube" placeholder="youtube_url"
              @change="migniature_video" v-model="this.urlyoutubeReconstruit">
          </div>
        </div>


        <div class="row" style="--bs-gutter-x: 0em;">
          <div class="input-group mb-3 ">
            <span class="input-group-text colovert" id="basic-addon2">vimeo_url :</span>
            <input type="text" class="form-control textfield" id="vimeo" placeholder="vimeo_url"
              @change="migniature_video" v-model="this.urlVimeoReconstruit">
          </div>
        </div>


        <div v-if="false" class="row" style="--bs-gutter-x: 0em;">
          <div class="input-group mb-3">
            <span class="input-group-text colovert">Audios :</span>
            <input list="Audiodata" id="choixAudio" name="choixAudio" class="form-control colovert"
              style="border: solid; border-color: var(--vert-midel);" v-model="laselectedAudio"
              @input="SelectedAudiosId">

            <datalist id="Audiodata">
              <option v-for="audio in listeAudios" :key="audio.id" :value="audio.name" :label="audio.name"> </option>
            </datalist>

            <button class="bt" type="button" @click="creerNouveauAudio"
              style="background-color: var(--gris-ultraclair);"> <img src="/imgs/add_black.svg" alt="add" class="col  ">
            </button>
          </div>

        </div>



        <div class="row" style="--bs-gutter-x: 0em;">
          <div class="input-group">
            <textarea type="aera" id="description" placeholder="Description"
              style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);"
              class="form-control" v-model="this.current_extrait.description"></textarea>
          </div>
        </div>

        <div v-if="!create" class="row" style="margin-right: 0em; margin-left: 0em;">
          <h1 class="row pcentrer"> Tableau des Playlist
          </h1>

          <table class="ultagger table tables table-striped">
            <thead>
              <tr>
                <th class="btgrisv2  col">Nom Playlist</th>
                <th class="btgrisv2  col">paramètre</th>
              </tr>
            </thead>
            <tbody class="tobodd">
              <tr class="col" v-for="interview in this.interviews">
                <td>
                  <RouterLink class="container container_extrait row " style="text-decoration: none; color: inherit;"
                    :to="'/admin/interview/' + interview.uuid"> {{ interview.titre }} </RouterLink>
                </td>
                <td>
                  <RouterLink class="container container_extrait col " style="text-decoration: none; color: inherit;"
                    :to="'/admin/interview/' + interview.uuid"> <button class="bt col"> modifier </button></RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="bottom_button">
      <RouterLink v-if="!create" to="/admin/extrait/" class="btn btn-outline-light"> <img src="/imgs/add.svg" alt="add">
        Ajouter un Extrait</RouterLink>
      <button @click="modificationDonnees()" type="button" class="btn btn-outline-success"> <img src="/imgs/save.svg"
          alt="Enregistrer"> Enregistrer </button>
      <button @click="this.popupDelete = true" type="button" class="btn  btn-outline-danger"> <img
          src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
    </div>

    <supprimer v-if="popupDelete" :Element_Supp="current_extrait" @closePopup="popupDelete = false" />

  </form>


  <!-- Only render tags when current_interview is loaded -->
  <tags v-if="current_extrait" :video="current_extrait" @update:tagsCreated="handleTagsCreated"
    @update:tagsDisconnected="handleTagsDisconnected" @update:tagsConnected="handleTagsConnected" />


  <div v-if="popupCreerQuestion">
    <popup_creer_question v-on:popupcreationquestion="popupchangequestion" :extraitUuid="this.current_extrait.uuid" />
  </div>


  <div v-if="popup">
    <popup_interview v-on:ecoutepopup="popupchange" />
  </div>


  <edit_success v-if="popupSuccess && create" message="Extrait créée !" />
  <edit_success v-else-if="popupSuccess && !create" message="Modification enregistrée !" />
  <edit_error v-if="popupError" :message="this.message_error" />


</template>

<style scoped>
.basemodif {
  width: 65%;
  height: 100%;
  padding: 1em;
}

.migniature {
  height: 90%;
  width: 90%;
}

.card {
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir));

  height: 553px;
  width: 470px;
}


.pad {
  padding-top: 1em;
  padding-bottom: 1em;
}

.pcentrer {
  margin-top: 1em;
  margin-bottom: 1em;
  justify-content: center
}

.centrer {
  justify-content: center
}

.tobodd {
  padding-top: 1em;
}

.tables {
  height: 1em;
  width: 100%;
}

.ultagger {
  list-style-type: none;

}

.grisetround {
  border-radius: 2em;

  background-color: var(--gris-moyen);
}

.grisee {
  background-color: var(--gris-moyen);
}


.textfield {
  background-color: var(--gris-ultraclair);
}

.bt {
  color: var(--blanc);
  background-color: var(--vert-pale);
  border-radius: 2em;
}

.colovert {
  border-color: var(--vert-pale);
  background-color: var(--vert-pale);
  color: var(--blanc);
}

.whiteelement {
  color: var(--blanc);
}

.migniature {
  border: solid 3px;
  border-color: var(--vert-neon);
  border-radius: 2em;

  height: 100%;
  width: 100%;
}

option {
  display: "none"
}

label {
  color: var(--vert-neon);
}


li>.card {
  padding: 20px 50px 150px;
  margin: 10px 10px 10px 10px;
}

span {
  min-width: 8em;
}

ul {
  display: flex;
  list-style-type: none;
  justify-content: space-between;
}


.scroller {
  width: 100%;
  height: 100vh;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}




.scroller2 {
  height: 100vh;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}




.button-blanc {
  background-color: var(--blanc);
}

.secondpart {
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: center;
  margin: 1em;
}
</style>
