<script>
import { mm_LegendClassMap } from '@model/mindmap/mm_const.js';
import mmch_Root from '@model/mindmap/mm_chemin_submod/mmch_root.js';

export default {
    name: "mindmap_node",
    props: {
        node_instance: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            mm_LegendClassMap: mm_LegendClassMap,
            nodeTitle: 'Titre Inconnue',
            nodeSubtitle: "Sous-Titre Inconnue",
            nodeDescription: ["Description Inconnue"],
            hasMiniature: false,
            thumbnailLoading: true,
            thumbnailUrl: "",
        };
    },
    mounted() {
        this.nodeSubtitle = this.mm_LegendClassMap[this.node_instance.constructor.mmch_dbjsclass.name] || 'Sous-Titre Inconnue';
        // if it's a category without data
        if (!this.node_instance.mmch_obj) {
            if (this.node_instance.constructor != mmch_Root) {
                this.nodeTitle = this.mm_LegendClassMap[this.node_instance.constructor.mmch_dbjsclass.name] || 'Titre Inconnue';
            } else {
                this.nodeTitle = '';
            }
            return;
        }
        // it's an object / video node
        this.thumbnailLoading = true;
        // load title
        this.node_instance.mmch_getTitle().then((title) => {
            if (title) this.nodeTitle = title;
        });
        // Load description
        this.node_instance.mmch_getDescription().then((descriptions) => {
            if (descriptions) this.nodeDescription = descriptions;
        });
        // Check if has miniature
        this.hasMiniature = this.node_instance.mmch_hasMiniature()
        if (this.hasMiniature) {
            this.node_instance.mmch_getMiniature().then((miniurl) => {
                if (miniurl) this.thumbnailUrl = miniurl;
                this.thumbnailLoading = false;
            });
        } else {
            this.thumbnailLoading = false;
        }
    },
}
</script>

<template>
    <div class="mm_node" :class="`mm_node ${this.node_instance.mmch_getStyle()}`"
        :style="this.node_instance.getStyle()">
        <!--
        <div style="display: none;">
            {{ this.node_instance }}
        </div>
        -->
        <template v-if="!this.node_instance.mmch_obj">
            <div class="mm_node_content">
                <p class="mm_node_title">{{ this.nodeTitle }}</p>
                <template v-if="this.node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
            </div>
        </template>
        <template v-else-if="this.node_instance.mmch_obj && hasMiniature">
            <div class="mm_node_content">
                <p class="mm_node_title">
                    {{ this.nodeTitle }}
                </p>
                <p class="mm_node_subtitle">{{ this.nodeSubtitle }}</p>
                <div class="mm_node_description">
                    <p v-for="(line, index) in this.nodeDescription" :key="index">
                        {{ line }}
                    </p>
                </div>
                <template v-if="this.node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
            </div>
            <div class="mm_node_preview">
                <template v-if="this.thumbnailLoading">
                    <img src="/imgs/spinner.gif" alt="Loading thumbnail..." class="mm_node_loading-spinner" />
                </template>
                <template v-else-if="this.thumbnailUrl">
                    <img :src="this.thumbnailUrl" alt="Miniature" class="mm_node_thumbnail">
                </template>
                <template v-else>
                    <img src="/imgs/close.svg" alt="erreur image" class="mm_node_no-thumbnail">
                </template>
            </div>
        </template>
        <template v-else-if="this.node_instance.mmch_obj && !hasMiniature">
            <div class="mm_node_content">
                <p class="mm_node_title">
                    {{ this.nodeTitle }}
                </p>
                <p class="mm_node_subtitle">{{ this.nodeSubtitle }}</p>
                <div class="mm_node_description">
                    <p v-for="(line, index) in nodeDescription" :key="index">
                        {{ line }}
                    </p>
                </div>
                <template v-if="this.node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
            </div>
        </template>
    </div>
</template>