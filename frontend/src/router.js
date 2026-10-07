import { createRouter, createWebHistory } from 'vue-router';
import ClientAPI from '@model/clientAPI';


// certaines pages  soient chargées légèrement en avance (par ex. la page de login ou la page admin),
//{ 
//  path: "/connection", 
//  component: () => import(/* webpackPrefetch: true */ "@views/connection.vue") 
//}

const admin_routes = {
  path: '/admin',
  meta: {
    admin: true,
  },
  children: [
    // Admin pages
    { path: "/admin", component: () => import(/* webpackPrefetch: true */"@views/admin/admin_acceuil.vue") },
    { path: "/admin/users", component: () => import(/* webpackPrefetch: true */"@views/admin/list/admin_liste_user.vue") },
    { path: "/admin/user/:id", component: () => import("@views/admin/edit/admin_details_user.vue") },
    { path: "/admin/interview", component: () => import("@views/admin/list/admin_liste_interview.vue") },
    { path: "/admin/interview/:id", component: () => import("@views/admin/admin_interview.vue") },
    { path: "/admin/extraits/", component: () => import("@views/admin/list/admin_liste_extrait.vue") },
    { path: "/admin/extrait/:id", component: () => import("@views/admin/edit/admin_edit_video.vue") },

    { path: "/admin/autres", component: () => import("@views/admin/autres.vue") },

    // creer admin
    { path: "/admin/user/", component: () => import("@views/admin/edit/admin_details_user.vue") },
    { path: "/admin/interview/creer/", component: () => import("@views/admin/admin_interview.vue") },
    { path: "/admin/extrait/", component: () => import("@views/admin/edit/admin_edit_video.vue") },
    { path: "/admin/:type/supprimer/:id", component: () => import("@views/admin/supprimer.vue") },
  ]
}


const routes = [
  // Pages principales
  { path: "/", component: () => import("@views/acceuil.vue") },
  { path: "/propos", component: () => import("@views/a_propos.vue") },
  { path: "/conditiongeneral", component: () => import("@views/condition_general.vue") },
  { path: "/account", component: () => import("@views/account.vue") },
  { path: "/connexion", component: () => import("@views/connexion.vue") },
  { path: "/inscription", component: () => import("@views/inscription.vue") },
  { path: "/reset-password", component: () => import("@views/reset_password.vue") },
  { path: "/lecteur_video/", component: () => import("@components/lecteur_video/lecteur_video.vue"), props: true },
  admin_routes,
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const user = ClientAPI.current_user;

  // Nécessite d'être admin et aucun utilisateur connecter
  if (to.meta.admin && !user) { return '/connexion'; }

  // Nécessite d'être admin et utilisateur non admin
  if (to.meta.admin && user && !user.is_admin) { return '/'; }
})

export default router;