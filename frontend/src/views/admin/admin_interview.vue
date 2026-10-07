<script>
import { markRaw } from 'vue';
import comp_baradmin from "@components/components_admin/nav_admin.vue";
import comp_petit_extrait from '@components/components_admin/Admin_presentation_petit_extrait.vue';
import supprimer from "./supprimer.vue";
import tags from "./tags.vue"
import edit_success from "./gestion/edit_success.vue"
import edit_error from './gestion/edit_error.vue';

import Interview from '@model/interview.js';
import Extrait from "@model/extrait.js";
import Tag from "@model/tag.js";
import Occasion from "@model/occasion.js"

import { handleTagsConnected, handleTagsDisconnected, handleTagsCreated } from './fn_save_tags.js';


export default {
    name: "page_admin_interview",
    components: {
        comp_baradmin,
        comp_petit_extrait,
        supprimer,
        tags,
        edit_success,
        edit_error
    },
    data() {
        return {
            Extraitlist: [],
            current_interview: null,
            current_list_extraits: [],
            tagsConnected: [],
            tagsToDisconnect: [],
            tagsToCreate: [],
            liste_occasion_bd: [],
            taillelist1: 0,
            taillelist2: 0,
            titre: '',
            occasion: null,
            name_occasion: '',
            description: '',
            popupDelete: false,
            popupSuccess: false,
            popupError: false,
            create: false,
            searchAvailable: "",
            searchPlaylist: "",
            chargement: false,
            createMode: false,
            message_error: '',
        };
    },
    computed: {
        filteredAvailableExtraits() {
            if (!this.searchAvailable) return this.Extraitlist

            return this.Extraitlist.filter(extrait =>
                extrait.titre?.toLowerCase().includes(
                    this.searchAvailable.toLowerCase()
                )
            )
        },

        filteredPlaylistExtraits() {
            if (!this.searchPlaylist) return this.current_list_extraits

            return this.current_list_extraits.filter(extrait =>
                extrait.titre?.toLowerCase().includes(
                    this.searchPlaylist.toLowerCase()
                )
            )
        }
    },


    methods: {
        /**
         * Démarre le drag d’un élément
         * configure les métadonnées (UUID + liste source) et initialise l’effet de déplacement.
         *
         * @param {DragEvent} evt - L’événement de dragstart.
         * @param {Object} item - L’élément extrait en cours de déplacement.
         * @param {string} sourceList - La liste d’origine ("available" ou "playlist").
         */
        startDrag(evt, item, sourceList) {
            // Empêche l'image / le lien d'être la "drag image"
            const crt = evt.currentTarget; // la div.drag-wrapper

            // Crée une copie invisible de la carte à utiliser comme drag image
            const clone = crt.cloneNode(true);
            clone.style.position = 'absolute';
            clone.style.top = '-9999px';
            clone.style.left = '-9999px';
            document.body.appendChild(clone);

            evt.dataTransfer.setDragImage(clone, 0, 0);

            // Remove after a short delay (Chrome needs async)
            setTimeout(() => document.body.removeChild(clone), 0);

            evt.dataTransfer.dropEffect = 'move';
            evt.dataTransfer.effectAllowed = 'move';
            evt.dataTransfer.setData('itemID', item.uuid);
            evt.dataTransfer.setData('sourceList', sourceList); // 'available' ou 'playlist'

        },

        /**
         * Autorise le drop en empêchant le comportement par défaut du navigateur.
         *
         * @param {DragEvent} evt - L’événement de dragover.
         */
        onDragOver(evt) {
            evt.preventDefault();
        },

        /**
         * Gère le drop d’un élément : récupère l’UUID, détermine la liste source/target,
         * déplace l’élément, calcule la position d’insertion dans la playlist si nécessaire,
         * et met à jour les compteurs ainsi que le rendu Vue.
         *
         * @param {DragEvent} evt - L’événement de drop.
         * @param {string} targetList - La liste cible ("available" ou "playlist").
         */
        onDrop(evt, targetList) {
            evt.preventDefault();



            const itemID = evt.dataTransfer.getData('itemID');       // UUID de l’élément drag
            const sourceList = evt.dataTransfer.getData('sourceList'); // 'available' ou 'playlist'

            let sourceArray = sourceList === 'playlist' ? this.current_list_extraits : this.Extraitlist;
            let targetArray = targetList === 'playlist' ? this.current_list_extraits : this.Extraitlist;

            // Trouver l’élément dans la liste source
            const itemIndex = sourceArray.findIndex(item => item.uuid === itemID);
            if (itemIndex === -1) return;

            const item = sourceArray.splice(itemIndex, 1)[0]; // supprime de la source

            if (targetList === 'playlist') {

                const targetItems = Array.from(evt.currentTarget.children);

                // Calcul de l'index d'insertion
                const dropY = evt.clientY;
                let insertIndex = targetArray.length; // par défaut fin
                for (let i = 0; i < targetItems.length; i++) {
                    const rect = targetItems[i].getBoundingClientRect();
                    if (dropY < rect.top + rect.height / 2) {
                        insertIndex = i;
                        break;
                    }
                }

                // Insérer à la bonne position
                targetArray.splice(insertIndex, 0, markRaw(item));

                // force vue à redessiner la liste playlist, sinon affichage non mis à jour car on change l'intérieurs de la liste et pas de changement de taille ...
                if (targetList === sourceList) {
                    // TRIGGER VUE RENDER 
                    // Forcer rerender sans proxifier les objets
                    this.current_list_extraits = this.current_list_extraits.map(e => markRaw(e));
                    this.Extraitlist = this.Extraitlist.map(e => markRaw(e));
                }
            } else if (targetList === 'available') {
                // ----------------------
                // Déplacer vers le début de la liste disponible
                // ----------------------
                targetArray.splice(0, 0, item);
            }

            // Mettre à jour les compteurs
            this.taillelist1 = this.Extraitlist.length;
            this.taillelist2 = this.current_list_extraits.length;

            // misa à jour des filtres de recherche
            const tmp_searchAvaible = this.searchAvailable;
            const tmp_searchPlaylist = this.searchPlaylist;
            this.searchAvailable = '';
            this.searchPlaylist = '';
            this.searchAvailable = tmp_searchAvaible;
            this.searchPlaylist = tmp_searchPlaylist;
        },

        handleTagsCreated(tags) {
            handleTagsCreated(this, tags)
        },

        handleTagsDisconnected(tags) {
            handleTagsDisconnected(this, tags)
        },

        handleTagsConnected(tag) {
            handleTagsConnected(this, tag)
        },

        async save_tags() {
            try {
                // Connecter les tags existants
                for (const tag of this.tagsConnected) {
                    await this.current_interview.connect_tag(tag);
                }

                // Créer et connecter les nouveaux tags
                for (const tagData of this.tagsToCreate) {
                    const newTag = await new Tag({ name: tagData.name }).create();
                    await this.current_interview.connect_tag(newTag);
                }

                // Déconnecter les tags
                for (const tag of this.tagsToDisconnect) {
                    await this.current_interview.disconnect_tag(tag);
                }

                // Réinitialiser les listes après sauvegarde
                this.tagsConnected = [];
                this.tagsToCreate = [];
                this.tagsToDisconnect = [];
            } catch (error) {
                console.error('Erreur lors de la sauvegarde des tags:', error);
                throw error;
            }
        },

        async save() {
            this.chargement = true;
            try {
                console.log("titre", this.titre)
                this.current_interview.titre = this.titre;
                // if(this.titre === ''){
                // //     throw new Error("Le titre est obligatoire")
                //     this.current_interview.titre = null;
                // }
                this.current_interview.description = this.description || '';

                // Find the tag in the available list
                const occas = this.liste_occasion_bd.find(o => o.name === this.name_occasion);
                if (occas) {
                    this.occasion = occas.uuid
                }
                else {
                    if (this.name_occasion) {
                        const occas_object = new Occasion({ 'name': this.name_occasion })
                        await occas_object.create()
                        this.occasion = occas_object.uuid
                    }
                    else {
                        throw new Error("Occasion ne doit pas être vide")
                    }

                }

                this.current_interview.occasion = this.occasion;

                let isCreate = this.create;
                if (isCreate) {
                    await this.current_interview.create();
                } else {
                    await this.current_interview.update();
                }
                await this.current_interview.setExtraits(this.current_list_extraits);
                await this.save_tags();

                // Stocker les flags AVANT le reload
                sessionStorage.setItem('popupSuccess', 'true');
                sessionStorage.setItem('create', isCreate ? 'true' : 'false');

                // Reload brutal
                window.location.href = `/admin/interview/${this.current_interview.uuid}`;

            } catch (error) {
                console.error('Erreur lors de la sauvegarde:', error.toString());
                this.message_error = error.toString();
                this.popupError = true;
                setTimeout(() => {
                    this.popupError = false;
                }, 5000)
                this.chargement = false;
            } finally {
                this.chargement = false;
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




        const InterviewId = this.$route.params.id;
        if (InterviewId) {
            this.current_interview = markRaw(await Interview.detail(InterviewId));

            // pré-remplissage du formulaire
            this.titre = this.current_interview.titre;
            this.description = this.current_interview.description;
            this.occasion = markRaw(await this.current_interview.occasion)
            this.name_occasion = this.occasion.name
            console.log("occasion", this.occasion)


            this.liste_occasion_bd = markRaw(await Occasion.list())

            this.current_list_extraits = markRaw(await this.current_interview.extraits({ 'order': 'APPARTIENT_A|position' }));
            this.taillelist2 = this.current_list_extraits.length;

            const allExtraits = markRaw(await Extrait.list());
            this.Extraitlist = markRaw(
                allExtraits.filter(e =>
                    !this.current_list_extraits.some(c => c.uuid === e.uuid)
                )
            );




        } else {
            this.create = true;
            this.current_interview = markRaw(new Interview({}));
            this.Extraitlist = allExtraits;
        }

        this.taillelist1 = this.Extraitlist.length;
    },

};
</script>

<template>
    <comp_baradmin />

    <div class="main_content">
        <h1 v-if="create" class="text-center"> Création d'une Playlist </h1>
        <h1 v-else class="text-center"> Modification d'une Playlist </h1>
        <input v-model="titre" class="form-control" placeholder="Titre (Obligatoire)" />
        <textarea type="aera" v-model="description" placeholder="Description" class="form-control"></textarea>
        <input v-model="name_occasion" class="form-control" placeholder="Occasion" list="occasionData" />
        <datalist id="occasionData">
            <option v-for="occasion in liste_occasion_bd" :key="occasion.uuid" :value="occasion.name" />
        </datalist>


        <div class="row row_gap">
            <div class="col-md-4 aggrandir div_extrait_dispo">
                <div class="pcentrer ">
                    <div class="row">
                        <h1> Disponible </h1>
                        <h2> Total Extraits : {{ this.taillelist1 }}</h2>
                    </div>

                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search..." v-model="searchAvailable" />
                        <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </button>
                    </div>

                    <ul class="drop-zone" @drop="onDrop($event, 'available')" @dragover="onDragOver($event)">
                        <li v-for="extraitv1 in filteredAvailableExtraits" :key="extraitv1.uuid" class="drag-el">
                            <div class="drag-wrapper" draggable="true"
                                @dragstart="startDrag($event, extraitv1, 'available')">
                                <comp_petit_extrait :current_extrait=extraitv1 />
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="col-md-4 aggrandir div_extrait_playlist">
                <div class="pcentrer ">
                    <div class="row">
                        <h1> Playlist</h1>
                        <h2> Total Extraits : {{ this.taillelist2 }}</h2>
                    </div>

                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search..." v-model="searchPlaylist" />
                        <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </button>
                    </div>

                    <ul class="drop-zone" @drop="onDrop($event, 'playlist')" @dragover="onDragOver($event)">
                        <li v-for="extraitv2 in filteredPlaylistExtraits" :key="extraitv2.uuid" class="drag-el">
                            <div class="drag-wrapper" draggable="true"
                                @dragstart="startDrag($event, extraitv2, 'playlist')">
                                <comp_petit_extrait :current_extrait=extraitv2 />
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- Only render tags when current_interview is loaded -->
        <tags v-if="current_interview" :video="current_interview" @update:tagsCreated="handleTagsCreated"
            @update:tagsDisconnected="handleTagsDisconnected" @update:tagsConnected="handleTagsConnected" />

        <div class="bottom_button">
            <RouterLink to="/admin/extrait/" class="btn btn-outline-light">
                <img src="/imgs/add.svg" alt="add"> Ajouter un Extrait
            </RouterLink>
            <RouterLink v-if="!create" to="/admin/interview/creer/" type="button" class="btn btn-outline-light">
                <img src="/imgs/add.svg" alt="add"> Ajouter une Playlist
            </RouterLink>
            <button @click="save()" type="submit" class="btn btn-outline-success">
                <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer
            </button>
            <button @click="this.popupDelete = true" type="button" class="btn btn-outline-danger">
                <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer
            </button>
        </div>
    </div>

    <supprimer v-if="popupDelete" :Element_Supp="current_interview" @closePopup="popupDelete = false" />
    <!-- BON - s'affiche SEULEMENT quand popupSuccess est true -->
    <edit_success v-if="popupSuccess && createMode" message="Playlist créée !" />
    <edit_success v-else-if="popupSuccess && !createMode" message="Modification enregistrée !" />
    <edit_error v-if="popupError" :message="this.message_error" />

    <div v-if="chargement" class="overlay">
        <img src="/imgs/spinner.gif" alt="loading image...">
    </div>
</template>

<style scoped>
/* marge globale pour le contenu */
.main_content {
    margin: 2%;
}

/* conteneur des deux colonnes */
.row_gap {
    display: flex;
    flex-wrap: nowrap;
    /* interdit le retour à la ligne */
    gap: 10%;
    /* espace entre les colonnes */
    margin: 2% 0% 2% 0%;
    /* marge pour ne pas coller aux bords */
    align-items: stretch;
    /* les colonnes ont la même hauteur */
}

/* colonnes */
.aggrandir {
    display: flex;
    flex-direction: column;
    flex: 1 1 0;
    /* peut grandir mais pas rétrécir en dessous */
    min-width: 300px;
    /* largeur minimale pour ne pas rétrécir */
    height: auto;
    /* hauteur basée sur la colonne la plus grande */
    border-radius: 5px;
    /* arrondit les bords */
    overflow: hidden;
    /* optionnel : évite que le contenu dépasse */
}

/* wrapper vertical qui contient header / search / liste */
.pcentrer {
    display: flex;
    flex-direction: column;
    height: 100%;
    /* occupe toute la hauteur de la colonne */
}

/* empêcher header et search de grandir */
.pcentrer>*:not(.drop-zone) {
    flex: 0 0 auto;
}


.drop-zone {
    flex: 1 1 auto;
    overflow-y: auto;
    /* scroll vertical */
    overflow-x: hidden;
    padding: 10px;
    list-style: none;
    margin: 0;
    overscroll-behavior: contain;
}

/* cacher scrollbar mais garder le scroll */
.drop-zone {
    overflow-y: auto;
    scrollbar-width: none;
    /* Firefox */
    -ms-overflow-style: none;
    /* IE / Edge legacy */
}

.drop-zone::-webkit-scrollbar {
    display: none;
    /* Chrome / Safari */
}


/* si tu veux que les li s'empilent verticalement */
.drop-zone .drag-el {
    display: block;
    margin-bottom: 8px;
    padding: 8px;
    cursor: move;
}

/* éviter que les enfants forcent la taille */
.pcentrer * {
    box-sizing: border-box;
}

/* drag wrapper visuel */
.drag-wrapper {
    cursor: grab;
}

.drag-wrapper:active {
    cursor: grabbing;
}

/* garde esthétique pour header et search */
.aggrandir .header-zone {
    padding-bottom: 8px;
}

/* outlines pour debugger (enlever en production) */
.aggrandir {
    flex: 0 0 45%;
    /* largeur fixe en % */
    max-height: 90vh;
    outline: 1px dashed rgba(0, 0, 0, 0.05);
}

.drop-zone {
    outline: 1px dashed rgba(0, 0, 0, 0.05);
}



/* couleurs ul */
.div_extrait_dispo {
    background-color: var(--vert-midel);
}

.div_extrait_playlist {
    background-color: var(--vert-pale);
}

textarea {
    border: solid 0.3em;
    border-color: var(--vert-pale);
}

h1 {
    text-align: center;
}

.aggrandir h1 {
    margin-top: 2%;
}
</style>
