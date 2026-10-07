import { shallowRef, ref } from 'vue';
import mmch_CheminT from './mm_chemin_submod/mmch_chemin.js';
import mm_Linkage from "./mm_linkage.js";
import mm_Node from './mm_node.js';
import { mm_interface_handleclick } from "./mm_funcs/mm_interface.js";

export default class mm_Mindmap {

    static min_zoom = 0.1;
    static max_zoom = 2.0;

    /** @type {Object} */
    vueobj;
    /** @type {Array<mm_Linkage>} */
    linkages;
    /** @type {Array<mm_Linkage>} */
    previewlinkages;
    /** @type {Map<Number,mmch_CheminT>} */
    node_data;
    /** @type {Array<Number>} */
    chemin;
    /** @type {Number} the key of the mmch_root node*/
    root_key = null;
    /** @type {boolean} */
    fullscreen = false;
    /** @type {boolean} */
    togglelegend = true;
    /** @type {number} */
    scale = 1.0;
    /** @type {number} */
    offx = 0;
    /** @type {number} */
    offy = 0;
    /** @type {number} */
    lastMouseX = 0;
    /** @type {number} */
    lastMouseY = 0;
    /** @type {number} */
    clickTimer = null;
    /** @type {boolean} */
    dragging = false;
    /** @type {String} */
    searchval = "";

    interview_current;
    extrait_current;

    /**
     * @param {Object} vueobj 
     * @param {any} interview_current 
     * @param {any} extrait_current 
     */
    constructor(vueobj, interview_current, extrait_current) {
        // vue object reference
        this.vueobj = vueobj;
        // funcs ref
        this.interview_current = interview_current;
        this.extrait_current = extrait_current;
        // mm chemin
        this.chemin = ref([]);
        this.reset();
    }

    /**
     * @returns json
     */
    toJSON() {
        return {
            // linkages: this.linkages,
            // node_data: this.node_data,
            chemin: this.chemin,
            fullscreen: this.fullscreen,
            togglelegend: this.togglelegend,
            scale: this.scale,
            offx: this.offx,
            offy: this.offy,
            lastMouseX: this.lastMouseX,
            lastMouseY: this.lastMouseY,
            clickTimer: this.clickTimer,
            dragging: this.dragging,
            searchval: this.searchval
        };
    }

    /**
     * reset mminfo links nodes previewlinks
     */
    reset() {
        // mm data
        this.linkages = ref([]);
        this.node_data = { "data": shallowRef(new Map()), "key": 0 };
        // mm preview data
        this.previewlinkages = ref([]);
    }

    /**
     * do update
     */
    update() {
        this.node_data["key"]++;
    }

    /**
     * add node to mminfo map
     * @param {mm_Node} node add node to mminfo map
     */
    node_add(node) {
        this.node_data["data"].set(node.mmch_key, node);
    }

    /**
     * get node to mminfo map
     * @param {Number} key 
     * @returns {mm_Node | null} the node || null
     */
    node_get(key) {
        if (!(this.node_data["data"].has(key))) {
            console.error(`key not in mindmap.node_data["data"] Map ${key}`);
            return null;
        }
        return this.node_data["data"].get(key);
    }

    /**
     * recursivly delete a child
     * @param {mmch_CheminT<T>} parent parent node 
     * @param {Number} categoryK the number key of the child to delete
     */
    node_delete(parent,categoryK){
        const index = parent.childrens.findIndex(k => k === categoryK);
        if (index === -1) {
            console.error(`key not in parent.childrens ${categoryK}`);
            return;
        }
        const child = this.node_get(categoryK);
        // recursivly delete childrens
        for (let child_key of child.childrens) {
            this.node_delete(child,child_key);
        }
        // delete child from parent
        parent.childrens.splice(index, 1);
        // delete child from mminfo map
        this.node_data["data"].delete(categoryK);
        // delete child linkages
        this.linkages.value = this.linkages.value.filter(linkage => linkage.source.mmch_key !== categoryK && linkage.target.mmch_key !== categoryK);
    }

    /**
     * center mm et draw root
     */
    draw_root() {
        this.centerMindmap();
        mm_interface_handleclick(this, null);
        this.centerOnNode(this.node_get(this.root_key));
    }

    /**
     * handleClick
     * @param {mm_Node} node 
     */
    handleClick(node) {
        this.centerOnNode(node);
        mm_interface_handleclick(this, node);
    }

    /**
     * toggleFullscreen
     */
    toggleFullscreen() {
        if (!this.offx || !this.offy) {
            this.centerMindmap();
            this.centerOnNode(this.node_get(this.root_key));
        }
        this.fullscreen = !this.fullscreen;
        const element = this.vueobj.$el;
        if (this.fullscreen) {
            if (element.requestFullscreen) {
                element.requestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    /**
     * clamped zoom in +
     */
    zoomin() {
        this.scale += 0.1;
        this.scale = Math.min(mm_Mindmap.max_zoom, this.scale);
        if (!this.offx || !this.offy) {
            this.centerMindmap();
            this.centerOnNode(this.node_get(this.root_key));
        }
    }

    /**
     * clamped zoom out -
     */
    zoomout() {
        this.scale -= 0.1;
        this.scale = Math.max(mm_Mindmap.min_zoom, this.scale);
        if (!this.offx || !this.offy) {
            this.centerMindmap();
            this.centerOnNode(this.node_get(this.root_key));
        }
    }

    /**
     * zoom reset
     */
    zoomreset() {
        this.scale = 1.2;
        if (!this.offx || !this.offy) {
            this.centerMindmap();
            this.centerOnNode(this.node_get(this.root_key));
        }
    }

    /**
     * handleWheel
     * @param {*} event 
     */
    handleWheel(event) {
        event.preventDefault();
        const delta = -Math.sign(event.deltaY) * 0.1;
        const newScale = Math.max(mm_Mindmap.min_zoom, Math.min(mm_Mindmap.max_zoom, this.scale + delta));

        // Adjust offsets to zoom toward mouse position
        const rect = event.currentTarget.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        const scaleFactor = newScale / this.scale;
        this.offx = mouseX - (mouseX - this.offx) * scaleFactor;
        this.offy = mouseY - (mouseY - this.offy) * scaleFactor;

        this.scale = newScale;
    }

    /**
     * center the mm on screen
     */
    centerMindmap() {
        const container = this.vueobj.$el;
        if (container) {
            this.offx = container.clientWidth / 2;
            this.offy = container.clientHeight / 2;
        }
    }

    /**
     * center mm on node
     * @param {mm_Node} node 
     */
    centerOnNode(node) {
        const container = this.vueobj.$el;
        // console.trace(node);

        if (container) {
            // Calculate target position to center the node
            const targetOffx = container.clientWidth / 2 - node.targetX * this.scale;
            const targetOffy = container.clientHeight / 2 - node.targetY * this.scale;

            // Animate over 3 second to the new position
            this.animateToPosition(targetOffx, targetOffy);
        }
    }

    /**
     * animate mm to node
     * @param {Number} targetOffx 
     * @param {Number} targetOffy 
     * @param {Number} duration 
     */
    animateToPosition(targetOffx, targetOffy, duration=1000) {
        const startOffx = this.offx;
        const startOffy = this.offy;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function for smooth animation
            const easeProgress = this.easeInOutCubic(progress);

            this.offx = startOffx + (targetOffx - startOffx) * easeProgress;
            this.offy = startOffy + (targetOffy - startOffy) * easeProgress;

            // Force hover state update by triggering a small, non-visible change
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                // Final position - force a complete repaint
                this.update();
            }
        };

        requestAnimationFrame(animate);
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    /**
     * start Drag
     * @param {*} event 
     */
    startDrag(event) {
        this.dragging = true;
        const { clientX, clientY } = this.getEventCoordinates(event);
        this.lastMouseX = clientX;
        this.lastMouseY = clientY;
        event.preventDefault();
    }

    /**
     * stop Drag
     */
    stopDrag() {
        this.dragging = false;
        if (!this.offx || !this.offy) {
            this.centerMindmap();
            this.centerOnNode(this.node_get(this.root_key));
        }
    }

    doDrag(event) {
        if (!this.dragging) return;
        event.preventDefault();
        if (event.type.includes('touch')) {
            event.stopPropagation();
        }

        const { clientX, clientY } = this.getEventCoordinates(event);
        const deltaX = clientX - this.lastMouseX;
        const deltaY = clientY - this.lastMouseY;

        this.offx += deltaX;
        this.offy += deltaY;

        this.lastMouseX = clientX;
        this.lastMouseY = clientY;
    }

    /**
     * Helper methods for mobile vs web events type
     * @param {*} event 
     * @returns clientX clientY
     */
    getEventCoordinates(event) {
        if (event.type.includes('touch')) {
            const touch = event.touches[0];
            return {
                clientX: touch.clientX,
                clientY: touch.clientY
            };
        }
        return {
            clientX: event.clientX,
            clientY: event.clientY
        };
    }
}