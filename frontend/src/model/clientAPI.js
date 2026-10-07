import Utilisateur from "@model/utilisateur";
import FetchError from "@model/errors/fetch_error";

/**
 * Classe client faisant le lien avec l'api
 */
export default class ClientAPI {
  static BASE_URL = "http://localhost:8000/";
  static #endpoints = null;
  static #current_user;
  static #listeners = new Set();

  static get current_user() {
    return this.#current_user;
  }
  static set current_user(utilisateur) {
    this.#current_user = utilisateur;
    for (const callback of this.#listeners) {
      try {
        callback(this.#current_user);
      } catch (error) {
        console.error("ClientAPI listener error", error);
      }
    }
  }

  /**
   * S'abonner aux changements de current_user.
   * callback(current_user) sera appelé immédiatement avec la valeur courante
   * Returns: une fonction unsubscribe
   * @param {function} callback
   * @returns {function}
   */
  static subscribe(callback) {
    if (typeof callback !== "function")
      throw new Error("callback must be a function");
    this.#listeners.add(callback);
    try {
      callback(this.#current_user);
    } catch (e) {
      console.error("ClientAPI subscribe initial callback error", e);
    }
    return () => {
      this.#listeners.delete(callback);
      return null;
    };
  }

  /**
   * Récupère le dictionnaire des endpoints de l'api
   * Si nom de endpoint renseigner, renvoie url du endpoint
   * @param {string} endpoint
   * @returns {Promise<Record<string, string>|string>}
   */
  static async endpoints(endpoint) {
    if (!this.#endpoints) {
      this.#endpoints = await this.get(`${this.BASE_URL}api/`);
    }
    return endpoint ? this.#endpoints[endpoint] : this.#endpoints;
  }

  /**
   * Construction de l'url detail
   * @param {string} url
   * @param {string} uuid
   * @returns {string}
   */
  static url_uuid(url, uuid) {
    return uuid ? `${url}${uuid}/` : url;
  }

  /**
   * Construction de l'url avec paramètres
   * @param {string} url
   * @param {Record<string, string|string[]>} args
   * @returns {string}
   */
  static url_query(url, args) {
    return args ? url + `?${new URLSearchParams(args)}` : url;
  }

  /**
   * Récupère le header, ajoute le token si connecter (non implémenter)
   * @param {boolean} withAuth
   * @returns {Promise<Record<string, string>>}
   */
  static get_headers(withAuth = false) {
    let headers = {};
    headers["Content-Type"] = "application/json";
    if (withAuth) {
      const token = this.get_token();
      if (token) headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
  }

  /**
   * Récupère le token d'authentification de l'utilisateur connecté (access)
   * @returns {string|null}
   */
  static get_token() {
    return localStorage.getItem("access");
  }

  /**
   * Récupère le refresh token
   * @returns {string|null}
   */
  static get_refresh_token() {
    return localStorage.getItem("refresh");
  }

  /**
   * Stocke access/refresh dans localStorage
   * @param {string|null} access
   * @param {string|null} refresh
   */
  static save_tokens(access, refresh = null, user = null) {
    if (access) localStorage.setItem("access", access);
    if (refresh) localStorage.setItem("refresh", refresh);
  }

  /**
   * Supprime tokens
   */
  static clear_tokens() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
  }

  /**
   * Tente de refresh l'access token à partir du refresh token.
   * Retourne true si succès, false sinon.
   * IMPORTANT: endpoint utilisé: /api/token/refresh/
   * @returns {Promise<boolean>}
   */
  static async tryRefresh() {
    const refresh = this.get_refresh_token();
    if (!refresh) return false;
    try {
      const res = await fetch(`${this.BASE_URL}api/login/refresh/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ refresh: refresh }),
      });
      if (!res.ok) {
        this.clear_tokens();
        return false;
      }
      const data = await res.json();
      // SimpleJWT renvoie { access: "..." }
      if (data.access) {
        this.save_tokens(data.access, refresh); // conserve le refresh existant
        return true;
      } else {
        this.clear_tokens();
        return false;
      }
    } catch (e) {
      console.error("Erreur lors du refresh token :", e);
      this.clear_tokens();
      return false;
    }
  }

  /**
   *
   * @param {string} methode (GET, POST, PATCH, DELETE)
   * @param {string} url
   * @param {Record<string, string|string[]>} args
   * @param {Object} data
   * @param {boolean} withAuth
   * @returns {Promise<Object>}
   */
  static async fetch(methode, url, args = null, data = null, withAuth = false) {
    if (args) url = this.url_query(url, args);

    const opts = {
      method: methode.toUpperCase(),
      headers: await this.get_headers(withAuth),
    };
    if (data) opts["body"] = data;

    let response = await fetch(url, opts);

    if (response.status === 401 && withAuth) {
      const refreshed = await this.tryRefresh();
      if (refreshed) {
        opts.headers = this.get_headers(true);
        response = await fetch(url, opts);
      } else {
        this.clear_tokens();
        throw new FetchError(response.status, await response.json(), response);
      }
    }

    if (!response.ok) {
      throw new FetchError(response.status, await response.json(), response);
    }

    // Si pas de contenu (204), retourne null
    if (response.status === 204) return null;

    // parse JSON response
    return await response.json();
  }

  /**
   * Fetch GET
   * @param {string} url
   * @param {Record<string, string|string[]>} args
   * @param {boolean} withAuth
   * @returns {Promise<Object>}
   */
  static async get(url, args = null, withAuth = true) {
    return await this.fetch("GET", url, args, null, withAuth);
  }

  /**
   * Fetch POST
   * @param {string} url
   * @param {Object} data
   * @param {boolean} withAuth
   * @returns {Promise<Object>}
   */
  static async post(url, data, withAuth = true, args = null) {
    return await this.fetch("POST", url, args, data, withAuth);
  }

  /**
   * Fetch PATCH
   * @param {string} url
   * @param {Object} data
   * @param {boolean} withAuth
   * @returns {Promise<Object>}
   */
  static async put(url, data, withAuth = true) {
    return await this.fetch("PATCH", url, null, data, withAuth);
  }

  /**
   * Fetch DELETE
   * @param {string} url
   * @param {boolean} withAuth
   * @returns {Promise<Object>}
   */
  static async delete(url, withAuth = true) {
    return await this.fetch("DELETE", url, null, null, withAuth);
  }

  /**
   * Connecte un utilisateur avec son pseudo ou son e-mail et son password à l'api
   * @param {string} pseudo_email
   * @param {string} password
   * @returns {Promise<Utilisateur>}
   */
  static async connectAPI(pseudo_email, password, stay_connected) {
    try {
      const res = await this.post(
        `${this.BASE_URL}api/login/`,
        JSON.stringify({ username: pseudo_email, password: password }),
      );
      this.save_tokens(res.access, res.refresh);
      this.current_user = new Utilisateur(await this.get(res.utilisateur));
      if (stay_connected) localStorage.setItem("user", this.current_user.uuid);
      else localStorage.removeItem("user");

      return this.current_user;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  /**
   * Déconnecte un utilisateur de l'application
   * @returns {void}
   */
  static disconnectAPI() {
    this.clear_tokens();
    this.current_user = null;
    return this.current_user;
  }

  /**
   * Permet d'envoyer un fichier via un formData
   * @param {string} url
   * @param {File} file
   * @param {boolean} withAuth
   * @returns {Promise<Object>} réposnse de l'api
   */
  static async sendFile(url, file, withAuth = true) {
    const formData = new FormData();
    formData.append("file", file);

    const headers = await this.get_headers(withAuth);

    // SUPPRIMER Content-Type
    delete headers["Content-Type"];

    const opts = {
      method: "POST",
      headers,
      body: formData,
    };

    let response = await fetch(url, opts);

    if (response.status === 401 && withAuth) {
      const refreshed = await this.tryRefresh();
      if (refreshed) {
        opts.headers = await this.get_headers(true);
        delete opts.headers["Content-Type"];
        response = await fetch(url, opts);
      } else {
        this.clear_tokens();
        throw new FetchError(response.status, await response.json(), response);
      }
    }

    if (!response.ok) {
      throw new FetchError(response.status, await response.json(), response);
    }

    if (response.status === 204) return null;

    return await response.json();
  }
}

// Reconnexion automatique si rester connecter
if (!ClientAPI.current_user) {
  const user = localStorage.getItem("user");
  if (user) {
    try {
      ClientAPI.current_user = await Utilisateur.detail(user);
    } catch (error) {}
  }
}
