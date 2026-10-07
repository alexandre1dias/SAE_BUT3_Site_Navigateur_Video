
# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).


## Organisation des services frontend

Ce projet frontend suit une structure modulaire pour séparer les responsabilités et faciliter la maintenance :

- `src/` : code source principal de l'application.
	- `src/components/` : composants Vue réutilisables.
	- `src/views/` : vues / pages utilisées par le routeur.
	- `src/model/` : modèles et services métiers (ici se trouvent les objets métier, clients API et la logique d'accès aux données).
	- `src/main.js` : point d'entrée de l'application (initialisation de l'app, du routeur).
	- `src/router.js` : configuration des routes de l'application.
	- `src/App.vue` : composant racine de l'application.

- `public/` : fichiers statiques servis tels quels (index.html, manifest, images publiques).
- `tests/` : tests unitaires et d'intégration (Vitest + testing-library).
- `vite.config.js` : configuration du build et des alias.

Principes importants :
- Les `services` encapsulent les appels réseau et la logique d'accès aux données. Ils retournent des objets ou des promesses que les composants ou les stores consomment.
- Les composants sont purement présentiels autant que possible ; la logique métier est déléguée aux `services` ou au `store`.
- Les appels à l'API centralisés facilitent la gestion des erreurs, du retry, et de l'authentification (injection des tokens).

## Scripts utiles

- Démarrer en développement : `npm run dev`
- Lancer les tests : `npm run test`
- Construire pour la production : `npm run build`
- Linter : `npm run lint` (si configuré)

this.current_extrait.duree =  0;
mettre en place avec une api plus tard

reutiliser callback pour validation


# Tests
Se placer dans frontnend 
- Run `npm run test` to execute the unit tests via [Vitest](https://vitest.dev/).
pour run  fichier spesifique : npm run test -- <file path>
