import Model from "@model/model.js";
import Extrait from "@model/extrait.js";

export default class Artiste extends Model {
    #name;
    #extraits;

    constructor({ uuid, name, extraits }) {
        super(uuid);
        this.#name = name;
        this.#extraits = extraits;
    }

    static get endpoint() { return "artistes"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.constructor.validateString(value, "name"); }

    async extraits(args) { return await this.fetchList(this.#extraits, Extrait, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#extraits = json.extraits;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        return json;
    }
}