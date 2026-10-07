import Model from "@model/model.js";
import Theme from "@model/theme.js";
import Extrait from "@model/extrait.js";

export default class Question extends Model {
    #texte;
    #theme;
    #extraits;
    #theme_uuid;

    constructor({ uuid, texte, theme, extraits }) {
        super(uuid);
        this.#texte = texte;
        this.#theme = theme;
        this.#extraits = extraits;
        this.#theme_uuid = null;
    }

    static get endpoint() { return "questions"; }

    get texte() { return this.#texte; }
    set texte(value) { this.#texte = Question.validateString(value, "texte"); }

    get theme() { return this.fetchDetail(this.#theme, Theme); }
    set theme(value) { this.#theme_uuid = Question.validateString(value, "theme_uuid"); }

    async extraits(args) { return await this.fetchList(this.#extraits, Extrait, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#texte = json.texte;
        this.#theme = json.theme;
        this.#extraits = json.extraits;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            texte: this.#texte,
            theme_uuid: this.#theme_uuid
        };
    }
}
