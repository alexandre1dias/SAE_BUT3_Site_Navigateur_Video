<script>
import ClientAPI from "@model/clientAPI.js";
import router from "@/router.js";
export default {
    name: "page_connexion",
    data() {
        return {
            loading: false,
            username: "",
            password: "",
            stay_connected: true,
        };
    },
    methods: {
        async login() {
            // Refaire pour plus beau et intuitif (Messages d'erreurs, etc...)
            this.loading = true;
            await ClientAPI.connectAPI(this.username, this.password, this.stay_connected);
            if (ClientAPI.current_user) {
                if (window.history.length > 1) {
                    router.go(-1);
                } else {
                    router.replace('/');
                }
            }
            this.loading = false;
        },
    },
};
</script>

<template>
    <div class="d-flex p-5 mx-5">
        <div class="f-flex flex-grow-1 p-5 mx-5">
            <h1 class="vert-neon text-center">Connexion</h1>
            <form @submit.prevent="login" class="local d-flex flex-column my-5">
                <label class="d-flex flex-column px-5 fw-bold fs-5">
                    Pseudo ou Adresse e-mail
                    <input v-model="username" type="text" required class="my-2 p-2 border rounded" />
                </label>
                <div class="d-flex flex-grow-1 gap-5 my-3 py-3">
                    <hr class="w-100 border-vert-neon border border-3">
                    </hr>
                    <hr class="w-25 border-vert-neon border border-3">
                    </hr>
                    <hr class="w-100 border-vert-neon border border-3">
                    </hr>
                </div>
                <label class="d-flex flex-column px-5 fw-bold fs-5">
                    Mot de passe
                    <input v-model="password" type="password" required class="my-2 p-2 border rounded" />
                </label>
                <label class="d-flex justify-content-center px-5 fw-bold fs-5 gap-5">
                    Rester connecter ?
                    <!-- Refaire le style de la checkbox -->
                    <div class="form-check form-switch">
                        <input v-model="stay_connected" type="checkbox" class="my-2 p-2 rounded form-check-input" />
                    </div>
                </label>
                <div class="d-flex flex-column align-items-center m-5 gap-3">
                    <button class="p-2 w-25 h-100 border-0 rounded bg-vert-pale text-white">
                        <img v-if="this.loading" src="/imgs/spinner.gif" alt="loading image..." class="w-25">
                        <span v-else="this.loading">Valider</span>
                    </button>
                    <!-- TODO -->
                    <a href="" class="p-2 text-white text-decoration-none fw-bold">Mot de passe oublié ?</a>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.local label {
    color: var(--blanc);
}

.border-vert-neon {
    border-color: var(--vert-neon) !important;
    opacity: 1;
}

.bg-vert-pale {
    background-color: var(--vert-pale);
}

input:-webkit-autofill {
    -webkit-box-shadow: 0 0 0 1000px #fff inset !important;
    /* remplace #fff par ta couleur */
    box-shadow: 0 0 0 1000px #fff inset !important;
    background-clip: padding-box !important;
    -webkit-text-fill-color: #000 !important;
    color: #000 !important;
    caret-color: #000 !important;
    transition: background-color 5000s ease-in-out 0s !important;
}
</style>