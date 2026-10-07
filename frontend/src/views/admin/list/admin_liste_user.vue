<script>
import { markRaw } from 'vue';
import comp_baradmin from '@components/components_admin/nav_admin.vue';

import Utilisateur from "@model/utilisateur.js";

export default {
    name: "page_admin_listuser",
    components: {
        comp_baradmin,
    }, data() {
        return {
            utilisateurs: { type: Utilisateur },
        };
    },

    async mounted() {

        this.utilisateurs = markRaw(await Utilisateur.list());
        // console.log("liste des utilisateurs")
        console.log(this.utilisateurs)
    },
};


</script>

<template>
    <comp_baradmin />
    <h1 class="text-center">Utilisateur</h1>
    <div class="row">
        <RouterLink to="/admin/user/" class="col btgris btn change"> Ajouter un utilisateur <img src="/imgs/add.svg"
                alt="ajouter"></RouterLink>
        <div class="container col">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search"
                        aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                        <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="main-triev2">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th class="btgrisv2 col">Pseudo</th>
                    <th class="btgrisv2 col">Nom</th>
                    <th class="btgrisv2 col">Prénom</th>
                    <th class="btgrisv2 col">État du compte</th>
                </tr>
            </thead>
        </table>
        <div class="tbody-wrapper">
            <table class="table table-striped">
                <tbody class="tobodd">
                    <tr v-for="utilisateur in utilisateurs" :key="utilisateur.uuid">
                        <td class="col-pseudo">
                            <RouterLink class="link-cell" :to="{ path: '/admin/user/' + utilisateur.uuid }"> {{
                                utilisateur.pseudo }} </RouterLink>
                        </td>
                        <td class="col-nom">
                            <RouterLink class="link-cell" :to="{ path: '/admin/user/' + utilisateur.uuid }"> {{
                                utilisateur.nom }} </RouterLink>
                        </td>
                        <td class="col-prenom">
                            <RouterLink class="link-cell" :to="{ path: '/admin/user/' + utilisateur.uuid }"> {{
                                utilisateur.prenom }} </RouterLink>
                        </td>
                        <td class="col-etat">
                            <RouterLink class="link-cell" :to="{ path: '/admin/user/' + utilisateur.uuid }"> <button
                                    class="bt"> Details </button> </RouterLink>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
body {
    background-color: var(--noir);
}

.main-triev2 {
    padding: 2em;
}


.tbody-wrapper {
    display: block;
    max-height: 60vh;
    overflow-y: auto;
    overflow-x: hidden;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}


.tbody-wrapper::-webkit-scrollbar {
    width: 8px;
}

.tbody-wrapper::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.tbody-wrapper::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
}

.tbody-wrapper::-webkit-scrollbar-thumb:hover {
    background: #555;
}


.table {
    width: 100%;
    margin: 0;
    table-layout: fixed;
}

.tbody-wrapper .table {
    display: table;
    width: 100%;
}

.tbody-wrapper tbody {
    display: table-row-group;
}

.tbody-wrapper tr {
    display: table-row;
}

.tbody-wrapper td {
    display: table-cell;
}


.col-pseudo,
th:nth-child(1) {
    width: 25%;
}

.col-nom,
th:nth-child(2) {
    width: 25%;
}

.col-prenom,
th:nth-child(3) {
    width: 25%;
}

.col-etat,
th:nth-child(4) {
    width: 25%;
}

.card {
    background-color: var(--gris-moyen);
    filter: drop-shadow(20px 13px 4px var(--noir));
}

li>.card {
    padding: 20px 50px 150px;
    margin: 10px 10px 10px 10px;
}

.table-striped {
    --bs-table-bg: var();
    --bs-table-striped-bg: var();
    --bs-table-color: #1a1a1a;
    --bs-table-striped-color: #1a1a1a;
}

ul {
    display: flex;
    list-style-type: none;
    justify-content: space-between;
}

.change {
    max-width: 16em;
    margin-left: 3em;
}

.btgris {
    color: white;
    background-color: var(--gris-moyen);
    border-radius: 2em;
    border: none;
}

.btgrisv2 {
    color: white;
    background-color: var(--gris-moyen);
    padding: 1em;
}

.tobodd {
    padding-top: 0;
}

.link-cell {
    text-decoration: none;
    color: inherit;
    display: block;
    width: 100%;
    padding: 0.5rem;
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

.buttonsearch {
    background-color: var(--vert-pale);
}
</style>
