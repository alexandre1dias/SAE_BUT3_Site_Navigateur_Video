import Extrait from "../../extrait.js";
import Occasion from "../../occasion.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Interview from "./mmch_interview.js";
import mmch_Theme from "./mmch_theme.js";

/**
 * @extends mmch_CheminT<Occasion>
 */
export default class mmch_Occasion extends mmch_CheminT {
    static mmch_dbjsclass = Occasion;
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
        if (!this.mmch_obj) throw new Error("mmch description occasion on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const Occasion = this.mmch_obj;

        if (Occasion.name) description.push(`occasion : ${Occasion.name}`);

        this.#description = description.length > 0 ? description : ["no description Occasion"];
        return this.#description;
    }
}