<script>
import { markRaw } from 'vue';



import Question from "@model/question";
import Theme from "@model/theme";


export default {
    name: "popup_creer_question",
    props: {
        popupCreerQuestion: {
            type: Boolean,
            required: true
        },

        extraitUuid: {
            type: String,
            required: true
        }

    }, data() {
        return {
            laselectedQuestion: "",
            laselectedTheme: "",
            laselectedThemeUuid: "",
            listeQuestion: [],
            listetheme: [],   //liste des Questions totals
        }
    },
    methods: {
        changement_etat_popup() {
            this.$emit('popupcreationquestion', !this.popupCreerQuestion)
        },

        async recupetheme() {
            //reccupere la liste des Themes
            this.listetheme = markRaw(await Theme.list());
        },

        async recupeQuestion() {
            //reccupere la liste des Questions
            this.listeQuestion = markRaw(await Question.list());
        },

        FoncSelectedTheme(event) {
            const value = event.target.value;
            this.laselectedTheme = value;

            const theme = this.listetheme.find(t => t.name === value);

            if (theme) {
                this.laselectedThemeUuid = theme.uuid;
                console.log("Theme trouvé :", theme.name, theme.uuid);
            } else {
                this.laselectedThemeUuid = null;
                console.log("Nouveau thème :", value);
            }
        },

        async creerNouvelleQuestion() {
            if (this.laselectedQuestion != "" && this.laselectedQuestion != null) {
                if (!this.listeQuestion.find(a => a.texte === this.laselectedQuestion)) {
                    const newQuestion = new Question({});
                    newQuestion.texte = await this.laselectedQuestion;
                    newQuestion.theme = await this.laselectedThemeUuid;
                    newQuestion.theme_uuid = await this.laselectedThemeUuid;
                    await newQuestion.create();
                    this.listeQuestion.push(markRaw(newQuestion));
                    alert('Question creer');
                    // Reload brutal
                    window.location.href = `/admin/extrait/${this.extraitUuid}`;
                } else {
                    console.log('question existe deja');
                }
            } else {
                alert('pas de champs null pour Question');
            }

        },

        async creerNouvelleTheme() {
            if (this.laselectedTheme != "" && this.laselectedTheme != null) {

                if (!this.listetheme.find(a => a.name === this.laselectedTheme)) {
                    const newTheme = await new Theme({});
                    newTheme.name = this.laselectedTheme;

                    await newTheme.create()
                    this.listetheme.push(newTheme);


                    alert('le Theme ' + newTheme.name + ' est creer'); // ← ERREUR ICI : newArtiste au lieu de newTheme
                } else {
                    alert('le Theme existe deja')
                }
            } else {
                alert('pas de champs null pour theme'); // ← Changé "artiste" en "theme"
            }

        },

        creerQuestion(e) {
            const value = e.submitter.value

            if (value == "envoyer") {
                alert("nous avons: " + value);
                this.$emit('popupcreationquestion', !this.popupCreerQuestion)
            } else {
                this.$emit('popupcreationquestion', !this.popupCreerQuestion)
            }

        }

    },
    emits: ["popupcreationquestion"],


    computed: {

    },

    async mounted() {
        this.recupetheme();
    }
};




</script>



<template>
    <div class="allmightygris" @click="changement_etat_popup"></div>

    <div class="grisee allmighty trie-tagsfoncer row">
        <div class="row collumpopu ">
            <h1 class="row"> creation d'une nouvelle question </h1>

            <form class="row" @submit.prevent="creerQuestion">
                <div style="--bs-gutter-x: 0em;">
                    <div class=" input-group mb-3">
                        <span class="input-group-text colovert" id="basic-addon3"> Question Name :</span>
                        <input list="Questiondata" id="question" name="question" class="form-control "
                            style="border: solid; border-color: var(--vert-midel);" v-model="laselectedQuestion" />

                        <datalist id="Questiondata">
                            <option v-for="question in listeQuestion" :key="question.id" :value="question.texte"
                                :label="question.texte"> </option>
                        </datalist>
                    </div>

                    <div class=" input-group mb-3">
                        <span class="input-group-text colovert" id="basic-addon3"> Question theme :</span>
                        <input list="Questiontheme" id="questiontheme" name="questiontheme" class="form-control"
                            style="border: solid; border-color: var(--vert-midel);" :value="laselectedTheme"
                            @input="FoncSelectedTheme" />

                        <datalist id="Questiontheme">
                            <option v-for="theme in listetheme" :key="theme.id" :value="theme.name" :label="theme.name">
                            </option>
                        </datalist>

                        <button class="bt" type="button" style="background-color: var(--gris-ultraclair);"
                            @click="creerNouvelleTheme"> <img src="/imgs/add_black.svg" alt="add" class="col ">
                        </button>
                    </div>

                    <button @click="creerNouvelleQuestion" type="button" class="btn btn-outline-success"> <img
                            src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>

                    <button @click="" type="button" class="btn  btn-outline-danger"> <img src="/imgs/delete.svg"
                            alt="Annuler"> Annuler </button>




                </div>
            </form>


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
span {
    min-width: 10em;
}

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

.colovert {
    border-color: var(--vert-pale);
    background-color: var(--vert-pale);
    color: var(--blanc);
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