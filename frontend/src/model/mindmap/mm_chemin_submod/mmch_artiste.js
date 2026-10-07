import Extrait from "@model/extrait.js";
import Artiste from "@model/artiste.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";

/**
 * @extends mmch_CheminT<Artiste>
 */
export default class mmch_Artiste extends mmch_CheminT {
    static mmch_dbjsclass = Artiste;
    /** @type {Array<String>} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_listinst_args, ...args };
        yield mmch_Extrait;
        // TODO : put recomendation algorithm here
        const recommend = await this.mmch_obj.extraits(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }
    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_searchinst_args, ...args };
        yield mmch_Extrait;
        // TODO : put recomendation algorithm here
        const recommend = await this.mmch_dbjsclass.search(finalArgs);
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
        if (!this.mmch_obj) throw new Error("mmch description artiste on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const artiste = this.mmch_obj;

        try {
            const extraits = await artiste.extraits({ ...this.constructor.mmch_default_listinst_args });
            if (extraits.length > 0) {
                description.push(`${extraits.length} extrait(s) disponible(s)`);
            }
        } catch (error) { console.warn(error); }

        this.#description = description.length > 0 ? description : ["no description artiste"];
        return this.#description;
    }
}