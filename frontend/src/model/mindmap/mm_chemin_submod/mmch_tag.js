import Extrait from "../../extrait.js";
import Tag from "../../tag.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Interview from "./mmch_interview.js";

/**
 * @extends mmch_CheminT<Tag>
 */
export default class mmch_Tag extends mmch_CheminT {
    static mmch_dbjsclass = Tag;
    /** @type {Array<String>} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_listinst_args, ...args };
        yield mmch_Extrait;
        yield mmch_Interview;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_searchinst_args, ...args };
        yield mmch_Extrait;
        yield mmch_Interview;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_previewinst(mminfo, args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async mmch_getDescription() {
        if (!this.mmch_obj) throw new Error("mmch description tag on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const tag = this.mmch_obj;

        if (tag.name) description.push(`tag : ${tag.name}`);

        this.#description = description.length > 0 ? description : ["no description tag"];
        return this.#description;
    }
}