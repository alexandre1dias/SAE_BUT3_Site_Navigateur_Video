import Extrait from "../../extrait.js";
import Question from "../../question.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Theme from "./mmch_theme.js";

/**
 * @extends mmch_CheminT<Question>
 */
export default class mmch_Question extends mmch_CheminT {
    static mmch_dbjsclass = Question;
    /** @type {Array<String>} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_listinst_args, ...args };
        yield mmch_Extrait;
        yield mmch_Theme;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_searchinst_args, ...args };
        yield mmch_Extrait;
        yield mmch_Theme;
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

    async mmch_getTitle() {
        if (!this.mmch_obj) throw new Error("mmch mmch_getTitle question on empty obj");
        const question = this.mmch_obj;
        return question.texte.substring(0, 50);
    }

    async mmch_getDescription() {
        if (!this.mmch_obj) throw new Error("mmch description question on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const question = this.mmch_obj;
        /// try {
        ///     const theme = await question.theme();
        ///     if (theme && theme.name) description.push(`Thème: ${theme.name}`);
        /// } catch (error) { console.warn(error); }

        this.#description = description.length > 0 ? description : ["no description question"];
        return this.#description;
    }
}