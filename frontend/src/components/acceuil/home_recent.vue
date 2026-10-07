<script>
import { markRaw } from 'vue';
import Interview from '@model/interview.js';
import miniature_video from '@components/lecteur_video/miniature_video.vue';

export default {
    name: "comp_recent",
    inject: ["interview_current", "extrait_current"],
    components: {
        miniature_video,
    },
    data() {
        return {
            failed: false,
            loading: true,
            interviews: [],
        };
    },
    mounted() {
        this.loading = true;
        Interview.list({"size" : 3,"order":"date"}).then((interviews) => {
            if (!interviews){
                this.failed = true;
            }
            this.interviews = markRaw(interviews);
            this.loading = false;
        }).catch((error) => {
            this.loading = false;
            this.failed = true;
            console.error(error);
        });
    },
    methods: {
        gotoInter(inter) {
            this.loading = true;
            this.interview_current.set(inter);
            inter.extraits().then((extraits) => {
                this.extrait_current.set(markRaw(extraits[0]));
                this.$router.push(`/lecteur_video/`);
            });
        },
    },
};
</script>

<template>
    <div class="local-flex">
        <h3 class="vert-neon">Interview Récente</h3>
        <div v-if="loading" v-for="i in [1, 2, 3]" :key="i" class="local">
            <img src="/imgs/spinner.gif" alt="loading image...">
            <p>loading ...</p>
        </div>
        <div v-else-if="failed" v-for="k in [1, 2, 3]" :key="k" class="local">
            <img src="/imgs/close.svg" alt="erreur image">
            <p>erreur</p>
        </div>
        <div v-else v-for="inter in this.interviews" :key="inter.uuid" class="local">

            <div @click="gotoInter(inter)">
                <p>{{ inter.titre }}</p>
                <miniature_video :video="inter" class="mini" />
                <p>{{ inter.description }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.mini {
    width: 90%;
    height: auto;
    border-radius: 10px;
    margin-bottom: 10px;
    cursor: pointer;
}

.local-flex {
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    gap: 20px;
    justify-content: space-evenly
}

.local {
    background: var(--gris-moyen);

    border: 3px solid var(--vert-neon);
    box-shadow: 8px 8px 3.2px 5px var(--vert-pale);
    border-radius: 20px;

    padding: 16px;
    min-width: 350px;
    min-height: 350px;
    max-width: 400px;
    /* flex: 1 1 200px; */
}

.local h3 {
    margin: 0 0 8px 0;
}
</style>