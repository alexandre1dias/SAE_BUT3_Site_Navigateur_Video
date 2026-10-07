<script>

import { markRaw } from 'vue';
import comp_baradmin from "@components/components_admin/nav_admin.vue";
import popup_valider from "@components/components_admin/popup_validation_creation.vue";
import Utilisateur from "@model/utilisateur.js";
import supprimer from "../supprimer.vue";
import edit_success from "../gestion/edit_success.vue"
import edit_error from '../gestion/edit_error.vue';
import Tags from '@model/tag.js';

export default {
    name: "page_admin_details_client",
    components: {
        comp_baradmin,
        popup_valider,
        supprimer,
        edit_success,
        edit_error

    }, data() {
        return {
            current_utilisateur: { type: Utilisateur },
            tags: { type: Tags },
            dico_Utilisateur: {},
            create: false,
            popupEnregistrer: false,
            popupDelete: false,
            popupSuccess: false,
            popupError: false,
            showPassword: false,
            recherches_questions: [],
            recherches_artistes: [],
            regarder_interviews: [],
            regarder_extraits: [],
            taillelist1: 0,
            taillelist2: 0,
        };
    },


    methods: {
        popupchangeEnregistrer() {
            //permet de changer l'etat de la popup Enregistrer
            this.popupEnregistrer = !this.popupEnregistrer

        },

        async validationUSER() {
            let erreur = "";
            if (this.current_utilisateur.pseudo == null || this.current_utilisateur.pseudo == "") {
                erreur += "il manque un pseudo  \n";
            } if (this.current_utilisateur.nom == null || this.current_utilisateur.nom == "") {
                erreur += "il manque un nom  \n";
            } if (this.current_utilisateur.email == null || this.current_utilisateur.email == "") {
                erreur += "il manque un email  \n";
            }
            return erreur;
        },

        changeAdmin() {
            this.current_utilisateur.is_admin = !this.current_utilisateur.is_admin;
        },

        async modificationDonnees() {
            if (this.create) {
                await this.enregistrer();
            } else {
                await this.Update();
            }
        },

        async enregistrer() {

            try {
                this.message_error = await this.validationUSER();

                if (this.message_error == "") {
                    this.popupEnregistrer = true;
                    await this.current_utilisateur.create();
                    //this.new_extrait = new markRaw(new Extrait({}));
                    sessionStorage.setItem('popupSuccess', 'true');
                    sessionStorage.setItem('create', this.create ? 'true' : 'false');
                    // Reload brutal
                    window.location.href = `/admin/user/${this.current_utilisateur.uuid}`;
                    alert("creer");
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
        togglePassword() {
            this.showPassword = !this.showPassword;
        },

        async Update() {
            try {
                this.message_error = await this.validationUSER();
                if (this.message_error == "") {
                    await this.current_utilisateur.update();
                    sessionStorage.setItem('popupSuccess', 'true');
                    sessionStorage.setItem('create', this.create ? 'true' : 'false');
                    // Reload brutal
                    window.location.href = `/admin/user/${this.current_utilisateur.uuid}`;

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
    },
    computed: {
        isAdmin() {
            return this.current_utilisateur.is_admin;
        }
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
        const utilisateurId = this.$route.params.id;
        if (utilisateurId != null) {
            //reccuperation de l'Extrait via l'id
            this.current_utilisateur = markRaw(await Utilisateur.detail(utilisateurId));
            this.recherches_artistes = (markRaw(await this.current_utilisateur.recherches_artistes()));
            this.regarder_interviews = (markRaw(await this.current_utilisateur.regarder_interviews()));
            this.regarder_extraits = (markRaw(await this.current_utilisateur.regarder_extraits()));
            this.recherches_questions = (markRaw(await this.current_utilisateur.recherches_questions()));
        } else {
            this.current_utilisateur = markRaw(await new Utilisateur({}));
            this.create = true;
        }
        this.tags = markRaw(await Tags.list());
    },
};



</script>

<template>
    <comp_baradmin />

    <h1 v-if="!create" class="text-center colorneon"> Éditer {{ this.current_utilisateur.pseudo }} </h1>
    <h1 v-else class="text-center colorneon"> Créer Utilisateur</h1>

    <form action="" class="grisee" style="padding: 1em;">
        <div class="row client">
            <div class="row client">

                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Pseudo"> Pseudo </span>
                    <input type="text" class="form-control" id="Pseudo" name="Pseudo" placeholder="Pseudo"
                        v-model="this.current_utilisateur.pseudo">
                </div>

                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Prénom">Prénom</span>
                    <input type="text" class="form-control row client" id="Prénom" name="Prénom" placeholder="Prénom"
                        v-model="this.current_utilisateur.prenom">
                </div>

            </div>

            <div class="row client">


                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Nom">Nom</span>
                    <input type="text" class="form-control row client" id="Nom" name="Nom" placeholder="Nom"
                        v-model="this.current_utilisateur.nom">
                </div>

                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Adresse">Adresse</span>
                    <input type="text" class="form-control row client " id="Adresse" name="Adresse"
                        placeholder="Adresse e-mail" v-model="this.current_utilisateur.email">
                </div>
            </div>

            <div v-if="create == true" class="row client">
                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Mot De Passe">Mot De Passe</span>

                    <input :type="showPassword ? 'text' : 'password'" class="form-control row client" id="Mot De Passe"
                        name="Mot De Passe" placeholder="Mot De Passe" v-model="this.current_utilisateur.password">
                    <button class="btn btn-outline-secondary colovert" type="button" @click="togglePassword">
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>

                </div>
            </div>

            <div class="row client">

                <div class="row" style="--bs-gutter-x: 0em;">
                    <div class=" input-group mb-3">
                        <span class="input-group-text colovert" id="basic-addon3"> ACTIVER ADMIN :</span>
                        <input type="checkbox" class="btn-check" id="btn-check" autocomplete="off" @click="changeAdmin"
                            disabled v-model="this.current_utilisateur.is_admin" :checked="isAdmin">
                        <label class="btn btn-outline-danger" for="btn-check">OUI</label>
                    </div>
                </div>


            </div>

        </div>
        <div class="row bottom_button client">

            <RouterLink v-if="!create" to="/admin/user/" class="btn btn-outline-light"> <img src="/imgs/add.svg"
                    alt="add">
                Ajouter un USER</RouterLink>

            <button @click="modificationDonnees()" type="button" class="btn btn-outline-success"> <img
                    src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>

            <button v-if="!this.current_utilisateur.is_admin && create == false" @click="this.popupDelete = true"
                type="button" class="btn  btn-outline-danger"> <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer
            </button>

            <button v-if="create" @click="$router.go(-1)" type="button" class="btn btn-outline-danger">
                <img src="/imgs/delete.svg" alt="Annuler"> Annuler
            </button>

        </div>
    </form>



    <supprimer v-if="popupDelete" :Element_Supp="current_utilisateur" @closePopup="popupDelete = false" />

    <div v-if="popupEnregistrer">
        <popup_valider v-on:popupenregistrer="popupchangeEnregistrer" />
    </div>

    <edit_success v-if="popupSuccess && create" message="User créée !" />
    <edit_success v-else-if="popupSuccess && !create" message="Modification enregistrée !" />
    <edit_error v-if="popupError" :message="this.message_error" />


</template>

<style scoped>
.bt {
    color: var(--blanc);
    background-color: var(--vert-pale);
    border-radius: 2em;
}

h2 {
    margin-top: 1em;
}

.btred {
    color: var(--blanc);
    background-color: var(--rouge);
    border-radius: 2em;
}

.grisee {
    background-color: var(--gris-moyen);
    margin-top: 5vh;
    margin-bottom: 5vh;
}

label {
    color: var(--blanc);
}

.colorneon {
    color: var(--vert-neon);
}

.pcentrer {
    margin-top: 1em;
    margin-bottom: 1em;
    justify-content: center;
}

.ultagger {
    list-style-type: none;
}

.tagsfully {
    width: 100%;
    height: 100%;
}

.test {
    margin: 1%;
    text-align: center;
}

.colovert {
    border-color: var(--vert-pale);
    background-color: var(--vert-pale);
    color: var(--blanc);
}

.client {
    margin-right: 0px;
    margin-left: 0px;
}


.input-group {
    height: 60px;
}

.input-group .form-control {
    height: 100%;
    font-size: 1.1rem;
}

.input-group-text {
    height: 100%;
    display: flex;
    align-items: center;
}

.input-group .btn {
    height: 100%;
}


.bottom_button .btn {
    height: 60px;
    font-size: 1.1rem;
}

label {
    color: var(--blanc);
    text-align: center;
    justify-content: center;
    align-content: center;
    padding-right: 1em;
    min-width: 5em;
}

form {
    margin: 1em;
}

.colorneon {
    color: var(--vert-neon);
}

span {
    min-width: 5em;
}
</style>
