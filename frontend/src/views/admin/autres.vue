<script>
import { markRaw } from 'vue';
import comp_baradmin from "@components/components_admin/nav_admin.vue";

import Tags from '@model/tag.js';
import Artistes from '@model/artiste.js';
import Questions from '@model/question.js';
import Themes from '@model/theme.js';

export default {
    name: "page_autres",

    components: {
        comp_baradmin,
    },
    data() {
        return {

            Tags: { type: Tags },
            dico_tags: {},

            Questions: { type: Questions },
            dico_questions: {},

            Artistes: { type: Artistes },
            dico_artistes: {},

            Themes: { type: Themes },

        };
    },
    async mounted() {
        // console.log("mounted admin interview list");
        this.Questions = markRaw(await Questions.list());
        this.Artistes = markRaw(await Artistes.list());

        this.Themes = markRaw(await Themes.list());

        this.Tags = markRaw(await Tags.list());

        console.log(this.Questions)

    },

};
</script>




<template>
    <comp_baradmin />

    <h1 class="text-center">Autres</h1>

    <div class="scroller2">
        <section class="row ligne">
            <h2 class="vert-neon">Questions</h2>

            <section class="row">

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Questions total</span>
                    <span class=" col input-group-text">{{ this.Questions.length }}</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Questions utiliser</span>
                    <span class=" col input-group-text">nb Questions utiliser</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Questions non utiliser</span>
                    <span class=" col input-group-text">nb Questions non utiliser</span>
                </section>

            </section>

            <section>
                <table class="ultagger table tables table-striped">
                    <thead>
                        <tr>
                            <th class="btgrisv2  col">Question</th>
                            <th class="btgrisv2  col">Theme</th>
                            <th class="btgrisv2  col">nb dans extraits</th>
                        </tr>
                    </thead>
                    <tbody class="tobodd scroller">
                        <tr class="col" v-for="question in this.Questions">
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ question.texte }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>


        </section>

        <section class="row ligne">
            <h2 class="vert-neon">Tags</h2>

            <section class="row">

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Tags total</span>
                    <span class=" col input-group-text">{{ this.Tags.length }}</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Tags utiliser</span>
                    <span class=" col input-group-text">nb Tags utiliser</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert"> nb Tags non utiliser </span>
                    <span class=" col input-group-text"> nb Tags non utiliser</span>
                </section>
            </section>

            <section>
                <table class="ultagger table tables table-striped">
                    <thead>
                        <tr>
                            <th class="btgrisv2  col">name</th>
                            <th class="btgrisv2  col">nb dans interviews</th>
                            <th class="btgrisv2  col">nb dans extraits </th>
                        </tr>
                    </thead>
                    <tbody class="tobodd scroller">
                        <tr class="col" v-for="tag in this.Tags">
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ tag.name }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>

        </section>

        <section class="row ligne">
            <h2 class="vert-neon">Artistes</h2>
            <section class="row">

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert"> nb Artistes total</span>
                    <span class=" col input-group-text ">{{ this.Artistes.length }}</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Artistes utiliser</span>
                    <span class=" col input-group-text ">nb Artistes utiliser</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Artistes non utiliser</span>
                    <span class=" col input-group-text ">nb Artistes non utiliser</span>
                </section>

            </section>

            <section>
                <table class="ultagger table tables table-striped">
                    <thead>
                        <tr>
                            <th class="btgrisv2  col">Artistes</th>
                            <th class="btgrisv2  col">nb dans extraits </th>
                            <th class="btgrisv2  col">nb dans interviews</th>
                        </tr>
                    </thead>
                    <tbody class="tobodd scroller">
                        <tr class="col" v-for="artiste in this.Artistes">
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ artiste.name }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>

        </section>


        <section class="row ligne">
            <h2 class="vert-neon">Themes</h2>
            <section class="row">

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert"> nb Themes total</span>
                    <span class=" col input-group-text ">{{ this.Themes.length }}</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Themes utiliser</span>
                    <span class=" col input-group-text ">nb Themes utiliser</span>
                </section>

                <section class="col input-group mb-3">
                    <span class=" col input-group-text colovert">nb Themes non utiliser</span>
                    <span class=" col input-group-text ">nb Themes non utiliser</span>
                </section>

            </section>

            <section>
                <table class="ultagger table tables table-striped">
                    <thead>
                        <tr>
                            <th class="btgrisv2  col">Thème</th>
                            <th class="btgrisv2  col">nb dans extraits </th>
                            <th class="btgrisv2  col">nb dans interviews</th>
                        </tr>
                    </thead>
                    <tbody class="tobodd scroller">
                        <tr class="col" v-for="theme in this.Themes">
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ theme.name }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container  row " style="text-decoration: none; color: inherit;"
                                    :to="'/admin/interview/'"> {{ }} </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>

        </section>
    </div>

</template>

<style scoped>
.vert-neon {
    color: var(--vert-neon);
    justify-self: center;
}


.scroller2 {

    height: 63vh;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}


.colovert {
    border-color: var(--vert-pale);
    background-color: var(--vert-pale);
    color: var(--blanc);
}

.local-flex {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    flex: 1 1 200px;
}

.ligne {
    border-radius: 20px;
    margin: 1em;
    background-color: var(--gris-moyen);
}

.logo {
    max-width: 100px;
}

.textfield {
    background-color: var(--gris-ultraclair);
}
</style>