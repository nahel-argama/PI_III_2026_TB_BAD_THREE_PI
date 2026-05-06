import LoginView from '@/views/Auth/LoginView.vue';
import RegisterView from '@/views/Auth/RegisterView.vue';
import LandingPage from '@/views/Landing/LandingPage.vue';
import CheckoutView from '@/views/Checkout/CheckoutView.vue';
import DashboardView from '@/views/Dashboard/DashboardView.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { requireGuest, requireAuth } from '@/router/guards';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage,
    },

    /**
     * ROTA DE REGISTRO
     * requireGuest: Apenas usuários não-autenticados podem acessar
     * Se já estiver logado, redireciona para home
     */
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      beforeEnter: requireGuest,
    },

    /**
     * ROTA DE LOGIN
     * requireGuest: Apenas usuários não-autenticados podem acessar
     * Se já estiver logado, redireciona para home
     */
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: requireGuest,
    },

    /**
     * ROTA DE CHECKOUT
     * requireAuth: Apenas usuários autenticados podem acessar
     * Se não estiver logado, redireciona para /login
     */
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView,
      beforeEnter: requireAuth,
    },

    /**
     * DASHBOARD
     * requireAuth: Apenas usuários autenticados podem acessar
     * O conteúdo interno se adapta ao perfil salvo no Pinia
     */
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      beforeEnter: requireAuth,
    },

    /**
     * TODO: Adicionar rotas protegidas quando tiver componentes/páginas
     * Exemplo:
     * {
     *   path: '/dashboard',
     *   name: 'dashboard',
     *   component: DashboardView,
     *   beforeEnter: requireAuth,
     * },
     * {
     *   path: '/perfil',
     *   name: 'perfil',
     *   component: PerfilView,
     *   beforeEnter: requireAuth,
     * },
     */
  ],
});

export default router;
