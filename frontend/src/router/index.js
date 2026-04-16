import LoginView from '@/views/Auth/LoginView.vue';
import RegisterView from '@/views/Auth/RegisterView.vue';
import LandingPage from '@/views/Landing/LandingPage.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage,
    },

    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
  ],
});

export default router;
