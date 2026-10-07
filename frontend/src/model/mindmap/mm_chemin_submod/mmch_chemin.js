import mm_Node from "../mm_node.js";

/**
 * @template dbjsclass
 */
export default class mmch_CheminT extends mm_Node {
    /** @type {dbjsclass} */
    static mmch_dbjsclass = null;

    static mmch_default_listcat_args = { size : 1 };
    static mmch_default_listinst_args = { size : 1 };

    static mmch_default_searchcat_args = { size : 1 };
    static mmch_default_searchinst_args = { size : 1 };

    static mmch_default_previewcat_args = { size : 1 };
    static mmch_default_previewinst_args = { size : 1 };
    /** @type {dbjsclass} */
    mmch_obj;
    /** @type {Number} */
    mmch_key;
    static #mmch_counter = 0;

    constructor(mminfo, x, y, depth, content) {
        if (new.target === mmch_CheminT) {
            throw new Error("Cannot instantiate abstract class mmch_CheminT");
        }
        super(mminfo, x, y, depth + 1);
        this.mmch_obj = content;
        this.mmch_key = mmch_CheminT.#mmch_counter;
        mmch_CheminT.#mmch_counter += 1;
    }

    static reset_key_counter(){
        mmch_CheminT.#mmch_counter = 0;
    }

    static async* mmch_listcat(args = {}) {
        if (this.mmch_dbjsclass === null) throw new Error("mmch_listcat must be defined in child");
        const finalArgs = { ...this.constructor.mmch_default_listcat_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await this.mmch_dbjsclass.list(finalArgs);
        for (const item of recommend) {
            yield { cls: this, content: item };
        }
    }

    async* mmch_listinst(args = {}) {
        throw new Error("mmch_listinst must be defined in child");
    }

    static async* mmch_searchcat(args = {}) {
        if (this.mmch_dbjsclass === null) throw new Error("mmch_searchcat must be defined in child");
        const finalArgs = { ...this.constructor.mmch_default_searchcat_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await this.mmch_dbjsclass.search(finalArgs);
        for (const item of recommend) {
            yield { cls: this, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        throw new Error("mmch_searchinst must be defined in child");
    }

    static async* mmch_previewcat(mminfo, args = {}) {
        if (this.mmch_dbjsclass === null) throw new Error("mmch_previewcat must be defined in child");
        const finalArgs = { ...this.constructor.mmch_default_previewcat_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await this.mmch_dbjsclass.list(finalArgs);
        for (const item of recommend) {
            yield { cls: this, content: item };
        }
    }

    async* mmch_previewinst(mminfo, args = {}) {
        throw new Error("mmch_previewinst must be defined in child");
    }

    toJSON() {
        return {
            mmch_dbjsclass: this.constructor.mmch_dbjsclass,
            mmch_obj: this.mmch_obj,
            ...super.toJSON(),
        };
    }

    mmch_getStyle() {
        return `mmLegendColorMap${this.constructor.mmch_dbjsclass.name}`;
    }

    async mmch_getTitle() {
        if (!this.mmch_obj) throw new Error("mmch mmch_getTitle generic on empty obj");
        const obj = this.mmch_obj;
        if (obj.name) return obj.name;
        if (obj.titre) return obj.titre;
        if (obj.pseudo) return obj.pseudo;
        return "Sans titre";
    }

    async mmch_getDescription() {
        console.warn("mmch_getDescription generic");
        return ["no description"];
    }

    mmch_hasMiniature() {
        return false;
    }

    async mmch_getMiniature() {
        throw new Error("mmch_getMiniature must be defined in child");
    }

    // Get style for rendering (using x/y for smooth animation)
    getStyle() {
        // TODO : REDO

        const isVideoContent = this.mmch_hasMiniature(); // this.isVideoContent();
        const nodeDimensions = isVideoContent ?
            { width: 400, height: 300 } : // Squircle dimensions
            { width: 200, height: 200 };  // Round dimensions

        const scaledWidth = nodeDimensions.width * this.mminfo.scale;
        const scaledHeight = nodeDimensions.height * this.mminfo.scale;
        const sizetext = 20*this.mminfo.scale;

        // Calculate position - adjust for node center using x/y (real positions)
        const scaledX = (this.x * this.mminfo.scale) - (scaledWidth / 2);
        const scaledY = (this.y * this.mminfo.scale) - (scaledHeight / 2);

        return {
            "left": (scaledX + this.mminfo.offx) + "px",
            "top": (scaledY + this.mminfo.offy) + "px",
            "width": scaledWidth + "px",
            "height": scaledHeight + "px",
            "font-size": sizetext + "px",
            "line-height": sizetext + "px",
        };
    }
}