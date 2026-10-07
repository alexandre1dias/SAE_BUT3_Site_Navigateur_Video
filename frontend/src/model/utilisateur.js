import Artiste from "@model/artiste.js";
import Extrait from "@model/extrait.js";
import Interview from "@model/interview.js";
import Model from "@model/model.js";
import Question from "@model/question.js";

export default class Utilisateur extends Model {
    #pseudo;
    #prenom;
    #nom;
    #email;
    #password;
    #is_admin;
    #recherches_artistes;
    #regarder_interviews;
    #regarder_extraits;
    #recherches_questions;

    constructor({ uuid, pseudo, prenom, nom, email, is_admin, recherches_artistes, regarder_interviews, regarder_extraits, recherches_questions }) {
        super(uuid);
        this.#pseudo = pseudo;
        this.#prenom = prenom;
        this.#nom = nom;
        this.#email = email;
        this.#is_admin = is_admin;
        this.#recherches_artistes = recherches_artistes;
        this.#regarder_interviews = regarder_interviews; // liste de prommesses d'interviews regarder par le user
        this.#regarder_extraits = regarder_extraits; // liste de prommesses d'extraits regarder par le user
        this.#recherches_questions = recherches_questions;
    }

    static get endpoint() { return "utilisateurs"; }

    get pseudo() { return this.#pseudo; }
    set pseudo(value) { this.#pseudo = this.constructor.validateString(value, "pseudo"); }

    get prenom() { return this.#prenom; }
    set prenom(value) { this.#prenom = this.constructor.validateString(value, "prenom"); }

    get nom() { return this.#nom; }
    set nom(value) { this.#nom = this.constructor.validateString(value, "nom"); }

    get email() { return this.#email; }
    set email(value) { this.#email = this.constructor.validateString(value, "email"); }

    get password() { return this.#password; }
    set password(value) { this.#password = this.constructor.validateString(value, "password"); } // hash à gérer côté backend

    get is_admin() { return this.#is_admin; }
    set is_admin(value) { this.#is_admin = !!value; }

    async recherches_artistes(args) { return await this.fetchList(this.#recherches_artistes, Artiste, args); }

    async regarder_interviews(args) { return await this.fetchList(this.#regarder_interviews, Interview, args); }

    async regarder_extraits(args) { return await this.fetchList(this.#regarder_extraits, Extrait, args); }

    async recherches_questions(args) { return await this.fetchList(this.#recherches_questions, Question, args); }

    /**
     * Connecte un utilisateur à un artiste
     * @param {Artiste} artiste 
     */
    connect_artiste(artiste) {
        this.connect(this.#recherches_artistes, { 'uuid': artiste.uuid });
    }

    /**
     * Déconnecte un utilisateur d'un artiste
     * @param {Artiste} artiste 
     */
    disconnect_artiste(artiste) {
        this.disconnect(this.#recherches_artistes, artiste);
    }

    /**
     * Connecte un utilisateur à une interview
     * @param {Interview} interview 
     */
    connect_interview(interview) {
        this.connect(this.#regarder_interviews, { 'uuid': interview.uuid });
    }

    /**
     * Déconnecte un utilisateur d'une interview
     * @param {Interview} interview 
     */
    disconnect_interview(interview) {
        this.disconnect(this.#regarder_interviews, interview);
    }

    /**
     * Connecte un utilisateur à un extrait
     * @param {Extrait} extrait 
     */
    connect_extrait(extrait) {
        this.connect(this.#regarder_extraits, { 'uuid': extrait.uuid });
    }

    /**
     * Déconnecte un utilisateur d'un extrait
     * @param {Extrait} extrait 
     */
    disconnect_artiste(extrait) {
        this.disconnect(this.#regarder_extraits, extrait);
    }

    /**
     * Connecte un utilisateur à une question
     * @param {Question} question 
     */
    connect_artiste(question) {
        this.connect(this.#recherches_questions, { 'uuid': question.uuid });
    }

    /**
     * Déconnecte un utilisateur d'une question
     * @param {Question} question 
     */
    disconnect_artiste(question) {
        this.disconnect(this.#recherches_questions, question);
    }

    fromJSON(json) {
        super.fromJSON(json);
        this.#pseudo = json.pseudo;
        this.#prenom = json.prenom;
        this.#nom = json.nom;
        this.#email = json.email;
        this.#is_admin = json.is_admin;
        this.#recherches_artistes = json.recherches_artistes;
        this.#regarder_interviews = json.regarder_interviews;
        this.#regarder_extraits = json.regarder_extraits;
        this.#recherches_questions = json.recherches_questions;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        if (this.pseudo) json['pseudo'] = this.pseudo;
        if (this.prenom) json['prenom'] = this.prenom;
        if (this.nom) json['nom'] = this.nom;
        if (this.email) json['email'] = this.email;
        if (this.password) json['password'] = this.password;
        if (this.is_admin) json['is_admin'] = this.is_admin;
        return json;
    }
}