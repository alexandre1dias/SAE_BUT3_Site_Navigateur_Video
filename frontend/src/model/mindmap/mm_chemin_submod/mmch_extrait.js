import Extrait from "../../extrait.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Artiste from "./mmch_artiste.js";
import mmch_Tag from "./mmch_tag.js";
import mmch_Interview from "./mmch_interview.js";
import mmch_Question from "./mmch_question.js";

/**
 * @extends mmch_CheminT<Extrait>
 */
export default class mmch_Extrait extends mmch_CheminT {
    static mmch_dbjsclass = Extrait;
    /** @type {String} */
    #previewurl = null;
    /** @type {Array<String>} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_listinst_args, ...args };
        yield mmch_Artiste;
        yield mmch_Tag;
        yield mmch_Interview;
        yield mmch_Question;

        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.constructor.mmch_default_searchinst_args, ...args };
        yield mmch_Artiste;
        yield mmch_Tag;
        yield mmch_Interview;
        yield mmch_Question;
        // TODO : put recomendation algorithm here
        
        const items = await Extrait.search(finalArgs);
        return [
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
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
        if (!this.mmch_obj) throw new Error("mmch description extrait on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const extrait = this.mmch_obj;
        
        ///try {
        ///    const question = await extrait.question();
        ///    if (question && question.texte) {
        ///        description.push(`Question: ${question.texte.substring(0, 50)}...`);
        ///    if (extrait.lieu) description.push(`Lieu: ${extrait.lieu}`);
        ///    }
        ///} catch (error) { console.warn(error); }
        ///
        ///try {
        ///    const artiste = await extrait.artiste();
        ///    if (artiste && artiste.name) description.push(`Artiste: ${artiste.name}`);
        ///} catch (error) { console.warn(error); }


        if (extrait.uploaded_at) {
            description.push(`Ajouté le: ${new Date(extrait.uploaded_at).toLocaleDateString()}`);
        }

        if (extrait.duree) {
            const minutes = Math.floor(extrait.duree / 60);
            const seconds = extrait.duree % 60;
            description.push(`Durée: ${minutes}:${seconds.toString().padStart(2, '0')}`);
        }

        try {
            const tags = await extrait.tags({ ...this.constructor.mmch_default_listinst_args });
            if (tags.length > 0) {
                const tagNames = tags.map(t => t.name).join(', ');
                description.push(`Tags: ${tagNames}`);
            }
        } catch (error) { console.warn(error); }

        this.#description = description.length > 0 ? description : ["no description extrait"];
        return this.#description;
    }

    async #get_url() {
        if (!this.mmch_obj) return null;
        if (this.#previewurl) return this.#previewurl;
        const extrait = this.mmch_obj;
        if (extrait.youtube_url) {
            this.#previewurl = extrait.url_miniature_yt;
        } else if (extrait.vimeo_url) {
            this.#previewurl = await extrait.get_url_miniature_vimeo();
        } else {
            throw new Error("unreachable Extrait doesn't have url");
        }
        return this.#previewurl;
    }

    mmch_hasMiniature() {
        if (!this.mmch_obj) return null;
        return true;
    }

    async mmch_getMiniature() {
        if (!this.mmch_obj) throw new Error("mmch mmch_getMiniature Extrait on empty obj");
        return await this.#get_url();
    }
}