import Model from "@model/model.js";
import Interview from "@model/interview.js";
import Extrait from "@model/extrait.js";

export default class Tag extends Model {
    #name;
    #interviews;
    #extraits;

    constructor({ uuid, name, interviews, extraits }) {
        super(uuid);
        this.#name = name;
        this.#interviews = interviews;
        this.#extraits = extraits;
    }

    static get endpoint() { return "tags"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    async interviews(args) { return this.fetchList(this.#interviews, Interview, args); }

    async extraits(args) { return this.fetchList(this.#extraits, Extrait, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#interviews = json.interviews;
        this.#extraits = json.extraits;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        return json;
    }
}
