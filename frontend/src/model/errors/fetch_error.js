export default class FetchError extends Error {
    #status;
    #detail;
    #response;

    /**
     * @param {number} status - Code HTTP
     * @param {string|Object} detail - Corps de l'erreur ou message brut
     * @param {Response} response - (optionnel) réponse brute du fetch
     */
    constructor(status, detail, response = null) {
        const message = typeof detail === 'string' ? detail : JSON.stringify(detail);
        super(`${status} : ${message}`);
        this.name = 'FetchError';

        this.#status = status;
        try {
            this.#detail = JSON.parse(detail);
        } catch {
            this.#detail = detail;
        }
        this.#response = response;
        this.message = this.toString();
    }

    get status() { return this.#status; }

    get detail() { return this.#detail; }

    get response() { return this.#response; }

    get isClient() { return this.status >= 400 && this.status < 500; }

    get isServer() { return this.status >= 500; }

    get isNotFound() { return (typeof this.detail == 'object' && this.status == 404 && 'Not Found' in this.detail); }

    get isUniqueProperty() { return (typeof (this.detail) == 'object' && this.status == 400 && 'Unique Property' in this.detail); }

    get isRequiredProperty() { return (typeof (this.detail) == 'object' && this.status == 400 && 'Required Property' in this.detail); }

    get isContextError() { return (typeof this.detail == 'object' && this.status == 400 && 'Context error' in this.detail); }

    get isAuthentification() { return (typeof this.detail == 'object' && this.status == 401 && 'detail' in this.detail); }

    get isPermission() { return (this.status == 403); }

    get isDataBaseOffline() { return (this.status == 503); }

    get isSerializerError() {
        return (
            this.status === 400 &&
            typeof this.detail === 'object' &&
            !Array.isArray(this.detail)
        );
    }

    formatSerializerErrors() {
        return Object.entries(this.detail)
            .map(([field, messages]) => {
                if (Array.isArray(messages)) { messages = messages.join(', '); }
                return `${messages.replaceAll('.', '')} : ${field}`;
            })
            .join('\n');
    }

    toString() {
        if (this.isClient) {
            if (this.isAuthentification) {
                return `Vous n'êtes pas connecté : ${this.detail['detail']}`;
            } else if (this.isNotFound) {
                return `L'élément recherché n'a pas été retrouvé : ${this.detail['Not Found']}`;
            } else if (this.isUniqueProperty) {
                return `La propriété suivantes est unique et existe déjà : ${this.detail['Unique Property']}`;
            } else if (this.isContextError) {
                return `L'élément recherché n'a pas été retrouvé : ${this.detail['Context error']}`;
            } else if (this.isPermission) {
                return `Vous n'avez pas la permission pour effectuer cette action`;
            } else if (this.isRequiredProperty) {
                return `La propriété ${this.detail['Required Property']} est requise`
            } else if (this.isSerializerError) {
                return this.formatSerializerErrors();
            }
            else {
                return this.detail;
            }
        } else if (this.isServer) {
            // Lorsque la connexion à l'API se réalise mais pas celle à la bd (non implémenté dans l'API)
            if (this.isDataBaseOffline) {
                return `La base de données n'est pas en ligne : ${this.detail}`;
            }
            return `Erreur serveur : [${this.status}] ${this.detail}`;
        } else {
            return `[${this.status}] ${this.detail ? JSON.stringify(this.detail) : this.message}`;
        }
        return this.response;
    }
}