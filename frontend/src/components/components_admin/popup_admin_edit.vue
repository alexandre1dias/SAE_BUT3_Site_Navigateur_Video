<script>
import { markRaw } from 'vue';
import Tags from '@model/tag.js';


import Interview from '@model/interview.js';

export default {
    name: "comp_admin_edit_popup",
    props: {
        popupSelectInterview: {
            type: Boolean,
            required: true
        }


    }, data() {
        return {
            interviews: { type: Interview },
            dico_interviews: {},
            tags: { type: Tags },
            interview_modifier: { type: Interview }
        };
    }, methods: {
        changement_etat_popup() {
            this.$emit('ecoutepopup', !this.popupSelectInterview)
        },


        ajouter_interview_parent() {
            if (this.interview_modifier == Interview) {
                this.$emit('Interview_ajouter', this.interview_modifier);
            }
        },


        retirer_interview_parent() {
            if (this.interview_modifier == Interview) {
                this.$emit('Interview_retirer', this.interview_modifier);
            }
        },


        tags_to_string(tags_array) {
            let string_tags = "";
            for (let tag of tags_array) {
                string_tags += tag.name + " ";
            }
            return string_tags.trim();
        },


    },
    emits: ["ecoutepopup"],


    async mounted() {
        this.interviews = markRaw(await Interview.list());
        this.tags = markRaw(await Tags.list())

        try {
            for (let interview of this.interviews) {
                this.dico_interviews[interview.uuid] = { "length": (await interview.extraits()).length, "tags": markRaw(await interview.tags()) };
            }

        } catch (error) {
            console.error('Erreur lors de la récupération des interviews ou des extraits:', error);
        }


    },

};




</script>



<template>
    <div class="allmightygris" @click="changement_etat_popup"></div>

    <div class="grisee allmighty trie-tagsfoncer row">
        <div class="col collumpopu ">

            <div class="container row fullwith" style="max-height: 4em;">
                <div class="search-bar">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search..." aria-label="Search"
                            aria-describedby="search-addon">
                        <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </button>
                    </div>
                </div>
            </div>


            <div class="row  trie-tags fullwith">

                <p class="row pcentrer ">Trier par tag</p>

                <ul class="scroller ultagger  tagsfully row">
                    <li class="col" v-for="tag in this.tags">
                        <button class="btn btn-primary"> {{ tag.name }} </button>
                    </li>
                </ul>
            </div>
        </div>

        <div class="col collumpopu ">

            <table class="scroller ultagger tableheight table tables table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Nom interview</th>
                        <th scope="col">Nb video</th>
                        <th scope="col">Tags</th>
                        <th scope="col">Ajouter</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="col" v-for="interview in this.interviews">
                        <td> {{ interview.titre }} </td>
                        <td> {{ this.dico_interviews[interview.uuid] ? this.dico_interviews[interview.uuid]["length"] :
                            null}} </td>
                        <td> {{ this.dico_interviews[interview.uuid] ?
                            tags_to_string(this.dico_interviews[interview.uuid]["tags"]) : null }} </td>
                        <td>
                            <button @click="ajouter_interview_parent" value="{{ interview }}"> add </button>
                            <button @click="retirer_interview_parent" value="{{ interview }}"> remove</button>
                        </td>

                    </tr>
                </tbody>
            </table>

        </div>
        <div class="col collx">
            <div class="row">
                <button type="button" class="btn-close btn-close-white" aria-label="Close"
                    @click="changement_etat_popup"></button>
            </div>
        </div>
    </div>





</template>

<style scoped>
.scroller {
    width: 300px;
    height: 100vh;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}

.tables {
    height: 1em;
    width: 100%;
}

.collumpopu {
    display: flex;
    flex-wrap: wrap;
    flex-grow: 1;
}

.collx {
    flex-grow: 0;
}

.tableheight {
    height: 100%;
}

.fullwith {
    width: 100%;
}

thead {
    height: 10%;
}

.tagsfully {
    width: 100%;
    height: 100%;
    flex-grow: 1;
}


.allmighty {
    display: flex;
    position: fixed;
    top: 50%;
    left: 50%;
    height: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    padding: 1em;
    border: 1em solid;
    border-color: var(--vert-neon);
    border-radius: 6px;
    width: 80%;
}

.allmightygris {
    position: fixed;
    top: 0%;
    left: 0%;
    height: 100%;
    width: 100%;
    z-index: 9998;
    padding: 1em;
    background-color: rgba(188, 212, 221, 0.521);
    cursor: pointer;
}

.ultagger {
    list-style-type: none;

}


.button-blanc {
    background-color: var(--blanc);
}


.trie-tagsfoncer {
    background-color: var(--gris-moyen);
}


.trie-tags {
    background-color: var(--gris-taupe);
}



.pcentrer {
    margin-top: 1em;
    margin-bottom: 1em;
    justify-content: center;
}

.search-bar {
    max-width: 500px;
    margin: auto auto;
}

.search-bar .input-group {
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.search-bar .form-control {
    border: none;
    padding-left: 20px;
}

.search-bar .btn {
    border: none;
    padding: 10px 20px;
}
</style>