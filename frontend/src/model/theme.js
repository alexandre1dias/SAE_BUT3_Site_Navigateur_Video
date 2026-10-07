import Model from "@model/model.js";
import Question from "@model/question.js";

export default class Theme extends Model {
    #name;
    #questions;

    constructor({ uuid, name, description, questions }) {
        super(uuid);
        this.#name = name;
        this.#questions = questions;
    }

    static get endpoint() { return "themes"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.constructor.validateString(value, "name"); }

    async questions(args) { return await this.fetchList(this.#questions, Question, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#questions = json.questions;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        return json;
    }
}
