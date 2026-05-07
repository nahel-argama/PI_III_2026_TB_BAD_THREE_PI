import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

/**
 * Composable useAuth - Interface simplificada para acessar o auth store
 *
 * Simplifica o acesso ao auth store em componentes.
 *
 * Uso:
 *   const auth = useAuth()
 *   // Depois usar: auth.isLoggedIn, auth.isLoading, auth.login(), auth.logout()
 */
export const useAuth = () => {
  const authStore = useAuthStore();

  /**
   * Login do usuário
   * @param {string} email
   * @param {string} password
   */
  const login = async (email, password) => {
    try {
      return await authStore.login(email, password);
    } catch (err) {
      throw err;
    }
  };

  /**
   * Logout do usuário
   */
  const logout = async () => {
    try {
      await authStore.logout();
    } catch (err) {
      console.error('Erro ao fazer logout:', err);
      throw err;
    }
  };

  /**
   * Computed reativo que obtém o nome do usuário
   */
  const userName = computed(() => authStore.getCurrentUser?.name || null);
  const userType = computed(() => authStore.getCurrentUserType || authStore.getCurrentUser?.type || null);

  return {
    // Direct store access for reactive props
    isLoggedIn: authStore.isLoggedIn,

    // Computed values
    userName, // String do nome (para {{ }})
    userType,

    // Methods
    login,
    logout,

    // Direct store access (if needed)
    authStore,
  };
};
