import { useAuthStore } from '@/stores/auth';

/**
 * Route Guard: requireAuth
 *
 * Protege rotas que requerem autenticação.
 * Se o usuário não estiver autenticado, redireciona para /login.
 *
 * Uso em router/index.js:
 * {
 *   path: '/dashboard',
 *   component: DashboardView,
 *   beforeEnter: requireAuth
 * }
 *
 * @param {object} to - Rota de destino
 * @param {object} from - Rota de origem
 * @param {function} next - Callback para prosseguir ou redirecionar
 */
export const requireAuth = (to, from, next) => {
  const authStore = useAuthStore();

  if (authStore.isLoggedIn) {
    // Usuário está autenticado, permite o acesso
    next();
  } else {
    // Usuário não está autenticado, redireciona para login
    next('/login');
  }
};

/**
 * Route Guard: requireGuest
 *
 * Protege rotas que só devem ser acessadas por usuários não-autenticados.
 * Por exemplo: /login, /register
 * Se o usuário já está autenticado, redireciona para a página inicial.
 *
 * Uso em router/index.js:
 * {
 *   path: '/login',
 *   component: LoginView,
 *   beforeEnter: requireGuest
 * }
 *
 * @param {object} to - Rota de destino
 * @param {object} from - Rota de origem
 * @param {function} next - Callback para prosseguir ou redirecionar
 */
export const requireGuest = (to, from, next) => {
  const authStore = useAuthStore();

  if (authStore.isLoggedIn) {
    // Usuário já está autenticado, redireciona
    next('/dashboard');
  } else {
    // Usuário não está autenticado, permite acesso
    next();
  }
};

/**
 * Route Guard: requireRole
 *
 * Protege rotas por role/tipo de usuário (futuro)
 *
 * TODO: Implementar quando o backend retornar tipos de usuário
 * Esperado: user_type normalizado para 'PRODUTOR' ou 'VAREJISTA'
 *
 * Uso:
 * { path: '/produtor/dashboard', beforeEnter: requireRole('PRODUTOR') }
 * { path: '/varejista/dashboard', beforeEnter: requireRole('VAREJISTA') }
 *
 * @param {string|array} requiredRoles - Role ou array de roles permitidas
 * @returns {function} - Função de guard
 */
export const requireRole = (requiredRoles) => {
  return (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.isLoggedIn) {
      // Usuário não autenticado
      next('/login');
      return;
    }

    const userRole =
      authStore.getCurrentUserType ||
      authStore.getCurrentUser?.user_type ||
      authStore.getCurrentUser?.type;
    const roles = Array.isArray(requiredRoles) ? requiredRoles : [requiredRoles];

    if (!roles.length || !requiredRoles) {
      next();
      return;
    }

    if (roles.includes(userRole)) {
      next();
      return;
    }

    next('/');
  };
};
