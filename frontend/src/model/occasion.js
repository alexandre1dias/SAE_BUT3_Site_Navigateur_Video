import Model from "@model/model.js";
import Interview from "@model/interview.js";

export default class Occasion extends Model {
    #name;
    #interviews;

    constructor({ uuid, name, interviews }) {
        super(uuid);
        this.#name = name;
        this.#interviews = interviews;
    }

    static get endpoint() { return "occasions"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    async interviews(args) { return await this.fetchList(this.#interviews, Interview, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#interviews = json.interviews;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        return json;
    }
}
