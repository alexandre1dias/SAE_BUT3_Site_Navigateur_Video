<script>
export default {
    name: "components_supprimer",
    props: {
        Element_Supp: {
            type: Object,
            required: true
        }
    },
    methods: {
        async deleteElement() {
            let chemin_redirection = "";

            if (this.Element_Supp.youtube_url != null || this.Element_Supp.vimeo_url != null) {
                chemin_redirection = "extraits";
            } else if (this.Element_Supp.titre != null || this.Element_Supp.titre != null) {
                chemin_redirection = "interview";
            } else if (this.Element_Supp.is_admin != null || this.Element_Supp.is_admin != null) {
                chemin_redirection = "user";
            }


            await this.Element_Supp.delete();
            this.$router.push(`/admin/${chemin_redirection}`);
        }
    },
    mounted() {
        console.log("elem sup", this.Element_Supp)
    },
    emits: ["closePopup"],
};
</script>

<template>
    <div class="overlay">
        <div class="popup">
            <h1> Voulez vous vraiment supprimer "{{ this.Element_Supp.titre }}" ? </h1>
            <button type="button" @click="$emit('closePopup')" class="col bt button-blanc"> Annuler </button>
            <button type="button" @click="deleteElement()" class="col bt button-blanc">Valider</button>
        </div>
    </div>
</template>

<style scoped>
.button-blanc {
    background-color: var(--blanc);
}
</style>
