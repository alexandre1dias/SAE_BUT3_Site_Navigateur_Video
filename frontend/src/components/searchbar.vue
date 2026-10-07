<script>
import { computed } from "vue";

export default {
    name: "comp_searchbar",
    inject: ["searchterm"],
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
            set(v) { this.searchterm.set(v); }
        }
    }
};
</script>

<template>
    <div class="recherche">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" v-model="searchValue" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <RouterLink to="/" class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </RouterLink>
                </div>
            </div>
        </div>

</template>



<style>
/*
.recherche{
    padding-top: 1em;
    padding-bottom: 1em;
}
*/
.buttonsearch{
    background-color: var(--vert-pale);
}


.search-bar {
    min-width: 200px;
    margin: auto auto;
}

.search-bar .input-group {
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.search-bar .form-control {
    border: none;
    margin: 0.1em;
}

.search-bar .btn {
    border: none;
}
</style>