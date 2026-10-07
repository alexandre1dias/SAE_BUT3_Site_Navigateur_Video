import Extrait from "../../extrait.js";
import Theme from "../../theme.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Question from "./mmch_question.js";

/**
 * @extends mmch_CheminT<Theme>
 */
export default class mmch_Theme extends mmch_CheminT {
    static mmch_dbjsclass = Theme;
    /** @type {Array<String>} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_listinst_args, ...args };
        yield mmch_Question;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_search_args, ...args };
        yield mmch_Question;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_previewinst(mminfo,parent,args = {}){
        const finalArgs = { ...this.constructor.mmch_default_preview_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async mmch_getDescription() {
        if (!this.mmch_obj) throw new Error("mmch description theme on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const theme = this.mmch_obj;

        if (theme.name) description.push(`theme : ${theme.name}`);

        this.#description = description.length > 0 ? description : ["no description theme"];
        return this.#description;
    }
}