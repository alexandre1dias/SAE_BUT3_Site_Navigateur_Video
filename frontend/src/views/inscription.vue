<script>
import { markRaw } from 'vue';
import Utilisateur from "@model/utilisateur.js";
import edit_success from "./admin/gestion/edit_success.vue"
import edit_error from './admin/gestion/edit_error.vue';

export default {
    name: "page_inscription",
    components: {
        edit_success,
        edit_error
    },

    data() {
        return {

            current_utilisateur: { type: Utilisateur },
            popupEnregistrer: false,
            popupDelete: false,
            popupSuccess: false,
            popupError: false,
            create: true,
            showPassword: false,

        };
    },


    methods: {
        async validationUSER() {
            let erreur = "";
            if (this.current_utilisateur.pseudo == null || this.current_utilisateur.pseudo == "") {
                erreur += "il manque un pseudo  \n";
            } if (this.current_utilisateur.nom == null || this.current_utilisateur.nom == "") {
                erreur += "il manque un nom  \n";
            } if (this.current_utilisateur.prenom == null || this.current_utilisateur.prenom == "") {
                erreur += "il manque un prenom  \n";
            } if (this.current_utilisateur.email == null || this.current_utilisateur.email == "") {
                erreur += "il manque un email  \n";
            } if (this.current_utilisateur.password == null || this.current_utilisateur.password == "") {
                erreur += "il manque un mot de passe  \n";
            }
            return erreur;
        },

        async Enregistrer() {
            try {
                this.message_error = await this.validationUSER();

                if (this.message_error == "") {
                    await this.current_utilisateur.create();
                    sessionStorage.setItem('popupSuccess', 'true');
                    sessionStorage.setItem('create', this.create ? 'true' : 'false');
                    window.location.href = `/connexion`;
                } else {
                    this.popupError = true;
                    setTimeout(() => {
                        this.popupError = false;
                    }, 5000)
                }


            } catch (error) {
                console.error('Erreur lors de l\'inscription:', error.toString());
                this.message_error = error.toString();
                this.popupError = true;
                setTimeout(() => {
                    this.popupError = false;
                }, 5000)
            }

        },


        togglePassword() {
            this.showPassword = !this.showPassword;
        }

    },

    async mounted() {

        // Popup succès après reload brutal
        if (sessionStorage.getItem('popupSuccess') === 'true') {
            this.popupSuccess = true;

            // Déterminer si c'était en mode création ou modification
            this.createMode = sessionStorage.getItem('create') === 'true';
            sessionStorage.removeItem('popupSuccess');
            sessionStorage.removeItem('create');

            // ⏱ cacher après 5 secondes
            setTimeout(() => {
                this.popupSuccess = false;
            }, 5000);
        }

        this.current_utilisateur = markRaw(await new Utilisateur({}));
    },
};



</script>

<template>
    <h1 class="vert-neon">Inscription</h1>
    <form action="" class="grisee" style="padding: 1em;">
        <div class="row client">
            <div class="row client">

                <div class="input-group mb-3 col">
                    <span class="row input-group-text  colovert client" for="Pseudo"> Pseudo </span>
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
                    <span class="row input-group-text  colovert client" for="Nom">Nom</span>
                    <input type="text" class="form-control row client" id="Nom" name="Nom" placeholder="Nom"
                        v-model="this.current_utilisateur.nom">
                </div>

                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Adresse">Adresse</span>
                    <input type="text" class="form-control row client " id="Adresse" name="Adresse"
                        placeholder="Adresse e-mail" v-model="this.current_utilisateur.email">
                </div>
            </div>

            <div class="row client">
                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Mot De Passe">Mot De Passe</span>

                    <input :type="showPassword ? 'text' : 'password'" class="form-control row client" id="Mot De Passe"
                        name="Mot De Passe" placeholder="Mot De Passe" v-model="this.current_utilisateur.password">
                    <button class="btn btn-outline-secondary colovert" type="button" @click="togglePassword">
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>

                </div>
            </div>

        </div>
        <div class="row bottom_button client">

            <button @click="Enregistrer()" type="button" class="btn btn-outline-success"> <img src="/imgs/save.svg"
                    alt="Enregistrer"> Enregistrer </button>
            <RouterLink class="btn  btn-outline-danger" to="/"> <img src="/imgs/delete.svg" alt="Supprimer"> Annuler
            </RouterLink>
        </div>
    </form>


    <edit_success v-if="popupSuccess && create" message="utilisateur créée !" />
    <edit_success v-else-if="popupSuccess && !create" message="Modification enregistrée !" />
    <edit_error v-if="popupError" :message="this.message_error" />

</template>

<style scoped>
.client {
    margin-right: 0px;
    margin-left: 0px;
}


.colovert {
    border-color: var(--vert-pale);
    background-color: var(--vert-pale);
    color: var(--blanc);
}

span {
    min-width: 5em;
}
</style>