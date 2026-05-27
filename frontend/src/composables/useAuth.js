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
    return await authStore.login(email, password);
  };

  /**
   * Logout do usuário
   */
  const logout = async () => {
    await authStore.logout();
  };

  /**
   * Computed reativo que obtém o nome do usuário
   */
  const userName = computed(() => authStore.getCurrentUser?.name || null);
  const userType = computed(
    () =>
      authStore.getCurrentUserType ||
      authStore.getCurrentUser?.user_type ||
      authStore.getCurrentUser?.type ||
      null,
  );

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
