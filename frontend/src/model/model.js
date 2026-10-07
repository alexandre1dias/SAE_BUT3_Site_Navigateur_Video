import ClientAPI from "@model/clientAPI.js";

/**
 * Classe par parent du Model
 */
export default class Model {
    #uuid;

    constructor(uuid) {
        this.#uuid = uuid;
    }

    /**
     * getter et setter de la classe
     */

    get uuid() {
        return this.#uuid;
    }

    /**
     *
     * Utiliser pour surcharger les données de l'instance
     * À surcharger dans les classes enfants avec les bonnes données
     * @param {Object} json
     * @returns {Promise<Model>}
     */
    fromJSON(json) {
        if (json && json.uuid !== undefined && json.uuid !== null) {
            this.#uuid = json.uuid;
        }
        return this;
    }

    /**
     * Utiliser pour récupérer les données de l'instance
     * À surcharger dans les classes enfants avec les bonnes données
     * @returns {Object}
     */
    toJSON(json = {}) {
        if (this.uuid) json['uuid'] = this.uuid;
        return json;
    }

    /**
     * Utiliser pour récupérer le nom de l'endpoint correspondant à la classe
     * À surcharger dans les classes enfants avec les bonnes données
     * @returns {string}
     */
    static get endpoint() {
        throw new Error("endpoint must be implemented by child class");
    }

    static format_duree(duree_seconds) {
        const hours = Math.floor(duree_seconds / 3600);
        const minutes = Math.floor((duree_seconds % 3600) / 60);
        const seconds = duree_seconds % 60;

        let formatted = "";
        if (hours > 0) formatted += String(hours).padStart(2, "0") + ":";
        formatted += String(minutes).padStart(2, "0") + ":";
        formatted += String(seconds).padStart(2, "0");
        return formatted;
    }

    // Peut-être avoir un validateDate ?

    /**
     * Vérifie que le type de la variable est le bon
     * @param {*} value
     * @param {string} fieldName
     * @param {string} type
     * @returns {*}
     */
    static validateType(value, fieldName, type) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`);
        }
        if (typeof value !== type) {
            throw new Error(`${fieldName} must be a ${type}, got ${typeof value}`);
        }
        return value;
    }

    /**
     * Valide si la valeur est un String
     * @param {*} value
     * @param {string} fieldName
     * @returns {string}
     */
    static validateString(value, fieldName) {
        return this.validateType(value, fieldName, "string");
    }

    /**
     * Valide si la valeur est un Int
     * @param {*} value
     * @param {string} fieldName
     * @returns {int}
     */
    static validateNumber(value, fieldName) {
        return this.validateType(value, fieldName, "number");
    }

    /**
     * Récupère l'instance de Class
     * @param {string} url
     * @param {Class} Class
     * @returns {Promise<Model>}
     */
    async fetchDetail(url, Class) {
        try {
            return new Class(await ClientAPI.get(url));
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    /**
     * Récupère la liste d'instances de Class
     * @param {string} url
     * @param {Class} Class
     * @returns {Promise<Array<Model>>}
     */
    async fetchList(url, Class, args = null) {
        try {
            return await ClientAPI.get(url, args).then((data) => {
                return data.map((row) => {
                    return new Class(row);
                });
            });
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    /**
     * Récupère la liste des éléments de this
     * @param {Record<string, string|string[]>} args
     * @returns {Promise<Array<Model>>}
     */
    static async list(args = null) {
        try {
            return await ClientAPI.get(
                await ClientAPI.endpoints(this.endpoint),
                args
            ).then((data) => {
                return data.map((row) => {
                    return new this(row);
                });
            });
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    /**
     * Permet de chercher dans la liste d'éléments
     * @param {string} search
     * @param {Record<string, string|string[]>} args
     * @returns {Promise<Array<Model>>}
     */
    static async search(search, args = null) {
        args ? (args["search"] = search) : (args = { search: search });
        return await this.list(args);
    }

    /**
     * Récupère l'élément de this à partir de son uuid
     * @param {string} uuid
     * @returns {Promise<Model>}
     */
    static async detail(uuid) {
        try {
            return await ClientAPI.get(
                ClientAPI.url_uuid(await ClientAPI.endpoints(this.endpoint), uuid)
            ).then((data) => {
                return new this(data);
            });
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    /**
     * Créé une instance de classe this
     * @returns {Promise<Model>}
     */
    async create() {
        if (this.#uuid) {
            throw new Error(
                `Cannot create ${this.constructor.name} that already has a UUID`
            );
        }
        return await ClientAPI.post(
            await ClientAPI.endpoints(this.constructor.endpoint),
            JSON.stringify(this.toJSON())
        )
            // Charger les nouvelles données dans l'instance
            .then((json) => {
                return this.fromJSON(json);
            });

    }

    /**
     * Modifie une instance de classe this
     * @returns {Promise<Model>}
     */
    async update() {
        if (!this.#uuid) {
            throw new Error(`Cannot update ${this.constructor.name} without a UUID`);
        }

        return await ClientAPI.put(
            ClientAPI.url_uuid(
                await ClientAPI.endpoints(this.constructor.endpoint),
                this.#uuid
            ),
            JSON.stringify(this.toJSON())
        )
            // Charger les nouvelles données dans l'instance
            .then((json) => {
                return this.fromJSON(json);
            });

    }

    /**
     * Supprime une instance de classe this
     * @returns {boolean}
     */
    async delete() {
        if (!this.#uuid) {
            throw new Error(`Cannot delete ${this.constructor.name} without a UUID`);
        }
        try {
            return await ClientAPI.delete(
                ClientAPI.url_uuid(
                    await ClientAPI.endpoints(this.constructor.endpoint),
                    this.#uuid
                )
            )
                // Charger les nouvelles données dans l'instance
                .then((result) => {
                    return true;
                });
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    /**
     * Connecte une instance à une autre instance
     * @param {string} url
     * @param {Object} data
     * @returns {Promise<Object>}
     */
    async connect(url, data) {
        try {
            return await ClientAPI.post(url, JSON.stringify(data));
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    /**
     * Déconnecte une instance d'une autre instance
     * @param {string} url
     * @param {Model} instance
     * @returns {Promise<Object>}
     */
    async disconnect(url, instance) {
        try {
            return await ClientAPI.delete(ClientAPI.url_uuid(url, instance.uuid));
        } catch (error) {
            console.error(error);
            return false;
        }
    }
}
