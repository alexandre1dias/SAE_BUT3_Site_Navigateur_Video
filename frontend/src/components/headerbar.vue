<script>
import comp_searchbar from './searchbar.vue';
import parametres_lecteur from './lecteur_video/parametres_lecteur.vue';
import { videoStore } from "@model/videoStore";
import ClientAPI from "@model/clientAPI.js";
import { markRaw } from 'vue';

export default {
    emits: ['set_lecteur'],
    name: "comp_headerbar",
    components: {
        comp_searchbar,
        parametres_lecteur,
    },
    data() {
        return {
            param_lecteur: false,
            current_user: null,
            unsubscribe_current_user: null,
        }
    },
    methods: {
        popup_param_lecteur() {
            this.param_lecteur = !this.param_lecteur
        },

        async set_lecteur(new_lecteur) {
            videoStore.lecteur = new_lecteur
            videoStore.iframeComponent.set_url(videoStore.lecteur)
        },

        disconnect() {
            ClientAPI.disconnectAPI();
        }

    },

    computed: {
        isconnected() {
            return !!(this.current_user && this.current_user.pseudo);
        },
        isadmin() {
            return !!(this.current_user && this.current_user.is_admin);
        }
    },

    mounted() {
        this.unsubscribe_current_user = ClientAPI.subscribe((u) => { this.current_user = u ? markRaw(u) : u; });
    },

    beforeUnmount() {
        if (this.unsubscribe_current_user) { this.unsubscribe_current_user = this.unsubscribe_current_user(); };
    }
};
</script>

<template>
    <header>
        <nav>
            <ul class="liste">
                <li class="btn local">
                    <RouterLink class="nav-link" to="/">Accueil</RouterLink>
                </li>
                <li style="flex-grow: 1;">
                    <comp_searchbar class="flex-grow-1" />
                </li>
                <li>
                    <img src="/imgs/Settings.svg" alt="paramètres" @click="popup_param_lecteur"></img>
                    <parametres_lecteur v-if="param_lecteur" @set_lecteur="this.set_lecteur($event)" />
                </li>
                <li class="btn local" v-if="isconnected && isadmin">
                    <RouterLink class="nav-link" to="/admin">Admin</RouterLink>
                </li>
                <li class="btn local" v-if="isconnected">
                    <RouterLink class="nav-link" to="/account">
                        <img src="/imgs/compte.svg" alt="compte">
                    </RouterLink>
                </li>

                <li class="btn local" v-if="!isconnected">
                    <RouterLink class="nav-link" to="/inscription">S'inscrire</RouterLink>
                </li>
                <li class="btn local" v-if="!isconnected">
                    <RouterLink class="nav-link" to="/connexion">Se Connecter</RouterLink>
                </li>
                <li class="btn local" v-if="isconnected">
                    <label class="nav-link" @click="disconnect">Déconnexion</label>
                </li>
            </ul>
        </nav>
    </header>
</template>

<style scoped>
.liste {
    gap: 2%;
    padding: 0.5em 1em 0.5em 2em;
    background-color: var(--gris-moyen);
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    align-content: center;
    justify-content: space-around;
    align-items: center;
}

.local {
    background-color: var(--vert-pale) !important;
    color: var(--blanc);
}

.local:hover {
    background-color: var(--vert-neon) !important;
}

ul {
    margin: 0;
    border-bottom: 3px solid var(--gris-taupe);
}

img {
    max-height: 1.5em;
    cursor: pointer;
}
</style>