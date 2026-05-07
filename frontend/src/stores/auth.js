import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

/**
 * Auth Store - Gerencia estado de autenticação centralizado
 *
 * Responsabilidades:
 * - Manter estado do usuário autenticado (token, dados do usuário)
 * - Persistir/carregar token de localStorage
 * - Ações de login, logout e inicialização
 * - Métodos para refresh token (TODO - quando backend implementar)
 */
export const useAuthStore = defineStore('auth', () => {
  // ===== STATE =====
  const token = ref(localStorage.getItem('token') || null);
  const user = ref(null);
  const userType = ref(null);

  // ===== GETTERS =====
  const isLoggedIn = computed(() => !!token.value);

  const getCurrentUser = computed(() => user.value);

  const getToken = computed(() => token.value);

  const getCurrentUserType = computed(() => userType.value || user.value?.type || null);

  // ===== PRIVATE METHODS =====

  /**
   * Salva token em localStorage de forma segura
   * @param {string} newToken - Token JWT a ser salvo
   */
  const _saveToken = (newToken) => {
    try {
      if (newToken) {
        localStorage.setItem('token', newToken);
        token.value = newToken;
      }
    } catch (err) {
      console.warn('Erro ao salvar token em localStorage:', err);
      throw err;
    }
  };

  /**
   * Carrega token de localStorage
   * @returns {string|null} - Token ou null se não existir
   */
  const _loadToken = () => {
    try {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        token.value = storedToken;
        return storedToken;
      }
      return null;
    } catch (err) {
      console.warn('Erro ao carregar token de localStorage:', err);
      return null;
    }
  };

  /**
   * Remove token de localStorage de forma segura
   */
  const _clearToken = () => {
    try {
      localStorage.removeItem('token');
      token.value = null;
    } catch (err) {
      console.warn('Erro ao limpar token de localStorage:', err);
    }
  };

  /**
   * Salva dados do usuário em localStorage e state
   * @param {object} userData - Dados do usuário a serem salvos
   */
  const _saveUserData = (userData) => {
    try {
      if (userData) {
        // Salva dados completos do usuário no state
        user.value = userData;
        userType.value = userData?.type || null;
      }
    } catch (err) {
      console.warn('Erro ao salvar dados do usuário:', err);
    }
  };

  /**
   * Decodifica o payload do JWT.
   * @param {string} jwt - Token JWT de acesso
   * @returns {object|null} - Payload decodificado
   */
  const _decodeJwtPayload = (jwt) => {
    try {
      if (!jwt) return null;

      const base64Url = jwt.split('.')[1];
      if (!base64Url) return null;

      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join(''),
      );

      return JSON.parse(jsonPayload);
    } catch (err) {
      console.warn('Erro ao decodificar payload do JWT:', err);
      return null;
    }
  };

  /**
   * Obtém o ID do usuário a partir do token JWT.
   * @param {string} jwt - Token JWT de acesso
   * @returns {number|null}
   */
  const _getUserIdFromToken = (jwt) => {
    const decodedToken = _decodeJwtPayload(jwt);
    const userId = decodedToken?.user_id || decodedToken?.userId || decodedToken?.id;

    return userId || null;
  };

  /**
   * Busca os dados completos do usuário autenticado no backend.
   * @param {string} jwt - Token JWT de acesso
   * @returns {Promise<object>} - Dados do usuário
   */
  const _fetchCurrentUser = async (jwt) => {
    const userId = _getUserIdFromToken(jwt);

    if (!userId) {
      throw new Error('ID do usuário não encontrado no token');
    }

    const { default: api } = await import('@/services/api');
    const response = await api.get(`/users/${userId}/`);
    _saveUserData(response.data);

    return response.data;
  };

  // ===== PUBLIC ACTIONS =====

  /**
   * Inicializa autenticação ao abrir a aplicação
   * Carrega token do localStorage se existir
   */
  const initializeAuth = async () => {
    try {
      const storedToken = _loadToken();
      if (!storedToken) {
        user.value = null;
        userType.value = null;
        return;
      }

      await _fetchCurrentUser(storedToken);
    } catch (err) {
      console.error('Erro ao inicializar autenticação:', err);
      clearAuth();
    }
  };

  /**
   * Realiza login do usuário
   * @param {string} email - Email do usuário
   * @param {string} password - Senha do usuário
   * @returns {object} - Dados retornados pelo backend
   * @throws {Error} - Se falhar no login
   */
  const login = async (email, password) => {
    try {
      // ===== NOTA IMPORTANTE =====
      // Aqui é feito o import dinâmico do api service para evitar
      // dependência circular (auth store → api → auth store)
      const { default: api } = await import('@/services/api');

      const payload = {
        email,
        password,
      };

      const response = await api.post('/users/login/', payload);
      const { access: accessToken, refresh: refreshToken, ...userData } = response.data;

      if (!accessToken) {
        throw new Error('Token não recebido do servidor');
      }

      // Salva token
      _saveToken(accessToken);
      await _fetchCurrentUser(accessToken);

      // TODO: Armazenar refresh token quando backend implementar refresh endpoint
      // localStorage.setItem('refresh_token', refreshToken);

      return response.data;
    } catch (err) {
      console.error('Erro no login:', err);
      throw err;
    }
  };

  /**
   * Faz logout do usuário
   * Limpa token, dados e redireciona para login
   */
  const logout = async () => {
    try {
      // TODO: Chamar backend endpoint de logout quando implementado
      // const { default: api } = await import('@/services/api');
      // await api.post('/users/logout/');

      clearAuth();
    } catch (err) {
      console.error('Erro ao fazer logout:', err);
      // Mesmo com erro, limpa o estado local
      clearAuth();
    }
  };

  /**
   * Limpa estado de autenticação completamente
   * Remove token e user data (sem redireção - deixa para o componente fazer)
   *
   * IMPORTANTE: Não redireciona aqui pois useRouter() não funciona em actions
   * A redireção é responsabilidade de quem chama (componente ou interceptor)
   */
  const clearAuth = () => {
    try {
      _clearToken();
      user.value = null;

      // Notifica outras abas sobre logout (via storage event)
      window.dispatchEvent(new Event('logout'));
    } catch (err) {
      console.error('Erro ao limpar autenticação:', err);
    }
  };

  /**
   * Define token a partir do armazenamento (por exemplo, após sincronizar entre abas)
   * @param {string} newToken - Novo token a ser definido
   * @param {object} userData - Dados do usuário
   */
  const setTokenFromStorage = (newToken, userData = null) => {
    if (newToken) {
      token.value = newToken;
      user.value = userData;
      userType.value = userData?.type || null;
    } else {
      token.value = null;
      user.value = null;
      userType.value = null;
    }
  };

  /**
   * Tenta renovar o token (refresh token)
   *
   * TODO: Implementar quando backend tiver endpoint de refresh
   * Esperado: POST /api/users/token/refresh/
   * Payload: { refresh: refreshToken }
   * Resposta: { access: newAccessToken }
   *
   * @returns {Promise<string>} - Novo token de acesso
   * @throws {Error} - Se falhar ao renovar
   */
  const refreshToken = async () => {
    // TODO: Implementar refresh token
    // const refreshTokenValue = localStorage.getItem('refresh_token');
    // if (!refreshTokenValue) {
    //   throw new Error('Refresh token não encontrado');
    // }
    //
    // const { default: api } = await import('@/services/api');
    // const response = await api.post('/users/token/refresh/', {
    //   refresh: refreshTokenValue,
    // });
    //
    // const newAccessToken = response.data.access;
    // _saveToken(newAccessToken);
    //
    // return newAccessToken;

    throw new Error('Refresh token não implementado. Backend não possui endpoint.');
  };

  // ===== SINCRONIZAÇÃO ENTRE ABAS =====
  // Escuta mudanças em localStorage para sincronizar logout/login entre abas
  if (typeof window !== 'undefined') {
    window.addEventListener('storage', (event) => {
      if (event.key === 'token') {
        // Se o token foi removido em outra aba, remove localmente também
        if (!event.newValue) {
          setTokenFromStorage(null);
        }
        // Se o token foi adicionado/alterado em outra aba, sincroniza
        else {
          setTokenFromStorage(event.newValue);
          _fetchCurrentUser(event.newValue).catch((err) => {
            console.warn('Erro ao sincronizar usuário entre abas:', err);
          });
        }
      }
    });

    // Sincronização via custom events (logout manual)
    window.addEventListener('logout', () => {
      token.value = null;
      user.value = null;
    });
  }

  return {
    // State
    token,
    user,
    userType,

    // Getters
    isLoggedIn,
    getCurrentUser,
    getToken,
    getCurrentUserType,

    // Actions
    initializeAuth,
    login,
    logout,
    clearAuth,
    setTokenFromStorage,
    refreshToken,
  };
});
