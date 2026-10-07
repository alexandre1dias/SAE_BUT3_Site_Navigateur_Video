import mm_Mindmap from "./mm_mindmap.js";
import mm_Node from "./mm_node.js";

export default class mm_Linkage {
    /** @type {mm_Node} */
    startnode;
    /** @type {mm_Node} */
    endnode;
    /** @type {number} */
    thickness;

    /**
     * 
     * @param {mm_Node} startnode 
     * @param {mm_Node} endnode 
     * @param {number} thickness 
     */
    constructor(startnode, endnode, thickness) {
        this.startnode = startnode;
        this.endnode = endnode;
        this.thickness = thickness;
    }

    toJSON() {
        return {
            startnode: this.startnode,
            endnode: this.endnode,
            thickness: this.thickness
        };
    }

    /**
     * @param {mm_Mindmap} mminfo 
     * @returns {String} CSS style for linkage
     */
    getStyle(mminfo) {
        const scaledStartX = this.startnode.x * mminfo.scale;
        const scaledStartY = this.startnode.y * mminfo.scale;
        const scaledEndX = this.endnode.x * mminfo.scale;
        const scaledEndY = this.endnode.y * mminfo.scale;

        const length = Math.sqrt(Math.pow(scaledEndX - scaledStartX, 2) + Math.pow(scaledEndY - scaledStartY, 2));
        const angle = Math.atan2(scaledEndY - scaledStartY, scaledEndX - scaledStartX) * 180 / Math.PI;

        return {
            "height": (this.thickness * mminfo.scale) + "px",
            "width": length + "px",
            "left": (scaledStartX + mminfo.offx) + "px", // 50 * scale to center
            "top": (scaledStartY + mminfo.offy) + "px", // 50 * scale to center
            "transform": `rotate(${angle}deg)`,
            "transform-origin": "0 50%",
        };
    }
}