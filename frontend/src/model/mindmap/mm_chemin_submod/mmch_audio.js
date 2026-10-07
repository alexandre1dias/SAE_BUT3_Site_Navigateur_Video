import Extrait from "@model/extrait.js";
import Audio from "@model/audio.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";

/**
 * @extends mmch_CheminT<Audio>
 */
export default class mmch_Audio extends mmch_CheminT {
    static mmch_dbjsclass = Audio;
    /** @type {Array<String>} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_searchinst_args, ...args };
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
        if (!this.mmch_obj) throw new Error("mmch description Audio on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const Audio = this.mmch_obj;

        if (Audio.name) description.push(`audio : ${Audio.name}`);

        this.#description = description.length > 0 ? description : ["no description Audio"];
        return this.#description;
    }
}