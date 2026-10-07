<script>
import { mm_LegendClassMap } from '@model/mindmap/mm_const.js';
import mm_Mindmap from '@model/mindmap/mm_mindmap.js';
import mindmap_node from './mindmap_node.vue';

export default {
    name: "comp_mindmap",
    inject: ["searchterm", "interview_current", "extrait_current"],
    components: {
        mindmap_node
    },
    data() {
        let inter = this.interview_current;
        let ext = this.extrait_current;
        return {
            mm_LegendClassMap: mm_LegendClassMap,
            mm_instance: new mm_Mindmap(this, inter, ext),
            searchval: "",
        };
    },
    mounted() {
        this.searchval = this.searchterm.get();
        this.mm_instance.searchval = this.searchval;
        this.mm_instance.centerMindmap();
        this.mm_instance.draw_root();
    },
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
        }
    },
    watch: {
        async searchValue(newVal) {
            this.searchval = newVal;
            this.mm_instance.searchval = this.searchval;
            await this.mm_instance.draw_root();
        }
    },
};
</script>

<template>
    <div class="mm_main_relative" @mousedown="mm_instance.startDrag" @mouseup="mm_instance.stopDrag"
        @mousemove="mm_instance.doDrag" @mouseleave="mm_instance.stopDrag" @wheel="mm_instance.handleWheel"
        @touchstart="mm_instance.startDrag" @touchend="mm_instance.stopDrag" @touchmove="mm_instance.doDrag">
        <button class="mm_fullscreenbtn" @click="mm_instance.toggleFullscreen" @touchend="mm_instance.toggleFullscreen">
            <img :src="mm_instance.fullscreen ? '/imgs/reduire.svg' : '/imgs/agrandir.svg'"
                :alt="mm_instance.fullscreen ? 'Exit fullscreen' : 'Enter fullscreen'" class="fullscreen-icon">
        </button>
        <div class="mm_control_outer">
            <div class="mm_controls">
                <button @click="mm_instance.zoomin()" @touchend="mm_instance.zoomin()">+</button>
                <button @click="mm_instance.zoomout()" @touchend="mm_instance.zoomout()">-</button>
                <button @click="mm_instance.zoomreset()" @touchend="mm_instance.zoomreset()">reset zoom</button>
                <button @click="mm_instance.centerOnNode(mm_instance.node_get(mm_instance.root_key))"
                    @touchend="mm_instance.centerOnNode(mm_instance.node_get(mm_instance.root_key))">recenter</button>
            </div>
            <div class="mm_legend_outer">
                <button v-if="mm_instance.togglelegend" @click="mm_instance.togglelegend = false;"
                    @touchend="mm_instance.togglelegend = false;">&gt</button>
                <button v-else @click="mm_instance.togglelegend = true;"
                    @touchend="mm_instance.togglelegend = true;">&lt</button>
                <transition name="mm_legend_anim">
                    <div class="mm_legend" v-if="mm_instance.togglelegend">
                        <div v-for="(nameproper, nameclass) in mm_LegendClassMap">
                            <div class="mm_legend_cercle" :class="`mmLegendColorMap${nameclass}`"></div>
                            <p>{{ nameproper }}</p>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
        <div v-for="link in mm_instance.linkages" :key="link.id" :style="link.getStyle(mm_instance)" class="mm_linkage">
        </div>
        <div v-for="link in mm_instance.previewlinkages" :key="link.id" :style="link.getStyle(mm_instance)"
            class="mm_linkage">
        </div>
        <div v-if="mm_instance.node_data" :key="mm_instance.node_data.key">
            <transition-group name="mm_node_outer" tag="div">
                <mindmap_node v-for="(val, key) in mm_instance.node_data.data" :key="key" :node_instance="val[1]"
                    @click="mm_instance.handleClick(val[1])" @touchend="mm_instance.handleClick(val[1])" />
            </transition-group>
        </div>
    </div>
</template>