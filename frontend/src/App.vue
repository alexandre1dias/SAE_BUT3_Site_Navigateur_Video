<script>
import { markRaw } from 'vue';
import comp_headerbar from '@components/headerbar.vue';
import comp_footerbar from '@components/footerbar.vue';
import global_popup from './views/admin/gestion/global_popup.vue';
import Interview from '@model/interview';
import Extrait from '@model/extrait';

export default {
    name: "page_router",
    components: {
        comp_headerbar,
        comp_footerbar,
        global_popup,
    },
    data() {
        return {
            searchterm: "", // text de recherche
            interview_current: markRaw({
            type: Interview,
            value: null,
            }),
            extrait_current: markRaw({
            type: Extrait,
            value: null,
            }),
            //  Ajouter des flags de chargement
            isLoadingInterview: false,
            isLoadingExtrait: false,
        }
        },

    provide() {
        return {
            searchterm: {
            get: () => this.searchterm,
            set: (value) => { this.searchterm = value }
            },
            interview_current: {
                get: async () => {
                    // Si déjà chargé, retourner directement
                    if (this.interview_current && this.interview_current.value) {
                        return this.interview_current;
                    }
                    
                    // Si en cours de chargement, attendre
                    if (this.isLoadingInterview) {
                        // Attendre que le chargement soit terminé
                        while (this.isLoadingInterview) {
                            await new Promise(resolve => setTimeout(resolve, 50));
                        }
                        return this.interview_current;
                    }
                    
                    // Charger une seule fois
                    const uuid = sessionStorage.getItem('interview_current');
                    if (uuid && uuid !== "null") {
                        this.isLoadingInterview = true;
                        try {
                            let tmp = markRaw(await Interview.detail(uuid));
                            this.interview_current = tmp;
                            return tmp;
                        } finally {
                            this.isLoadingInterview = false;
                        }
                    }
                    else{
                        console.error("pas d'uuid, repasse par l'acceuil pour choisir une video");
                    }
                    
                    return null;
                },
                
                set: (value) => {
                    this.interview_current = value ? markRaw(value) : null;
                    sessionStorage.setItem('interview_current', 
                    this.interview_current?.uuid || null);
                }
            },
            
            extrait_current: {
                get: async () => {
                    // Même logique pour extrait
                    if (this.extrait_current.value) {
                        return this.extrait_current;
                    }
                    
                    if (this.isLoadingExtrait) {
                        while (this.isLoadingExtrait) {
                            await new Promise(resolve => setTimeout(resolve, 50));
                        }
                        return this.extrait_current;
                    }
                    
                    const uuid = sessionStorage.getItem('extrait_current');
                    if (uuid && uuid !== "null") {
                        this.isLoadingExtrait = true;
                        try {
                            let tmp = markRaw(await Extrait.detail(uuid));
                            this.extrait_current = tmp;
                            return tmp;
                        } finally {
                            this.isLoadingExtrait = false;
                        }
                    }
                    
                    return null;
                },
                
                set: (value) => {
                    this.extrait_current = value ? markRaw(value) : null;
                    sessionStorage.setItem('extrait_current', 
                    this.extrait_current?.uuid || null);
                }
            },
        }
        },
}
</script>

<template>
    <comp_headerbar />
    <main>
        <router-view :key="$route.fullPath"></router-view>
        <!--
            <router-view v-slot="lecteur_video">
            <keep-alive>
                <Lecteur_video :is="lecteur_video" />
            </keep-alive>
        -->
    </main>
    <comp_footerbar />

    <global_popup/>
</template> 