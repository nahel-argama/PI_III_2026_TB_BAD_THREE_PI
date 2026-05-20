import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

/**
 * Auth Store - Gerencia estado de autenticação centralizado
 *
 * Responsabilidades:
 * - Manter estado do usuário autenticado (token, dados do usuário)
 * - Persistir/carregar tokens de localStorage
 * - Ações de login, signup, logout e inicialização
 * - Renovação de access token com refresh token
 */
export const useAuthStore = defineStore('auth', () => {
  const ACCESS_TOKEN_KEY = 'token';
  const REFRESH_TOKEN_KEY = 'refresh_token';
  const USER_TYPE_MAP = {
    PRODUCER: 'PRODUTOR',
    RETAILER: 'VAREJISTA',
  };

  const _normalizeUserType = (value) => USER_TYPE_MAP[value] || value || null;

  // ===== STATE =====
  const token = ref(localStorage.getItem(ACCESS_TOKEN_KEY) || null);
  const refreshTokenValue = ref(localStorage.getItem(REFRESH_TOKEN_KEY) || null);
  const user = ref(null);
  const userType = ref(null);

  // ===== GETTERS =====
  const isLoggedIn = computed(() => !!token.value);
  const getCurrentUser = computed(() => user.value);
  const getToken = computed(() => token.value);
  const getCurrentUserType = computed(() =>
    _normalizeUserType(userType.value || user.value?.user_type || user.value?.type),
  );

  // ===== PRIVATE METHODS =====

  const _saveToken = (newToken) => {
    if (newToken) {
      localStorage.setItem(ACCESS_TOKEN_KEY, newToken);
      token.value = newToken;
    }
  };

  const _saveRefreshToken = (newRefreshToken) => {
    if (newRefreshToken) {
      localStorage.setItem(REFRESH_TOKEN_KEY, newRefreshToken);
      refreshTokenValue.value = newRefreshToken;
    }
  };

  const _loadToken = () => {
    try {
      const storedToken = localStorage.getItem(ACCESS_TOKEN_KEY);
      if (storedToken) {
        token.value = storedToken;
        return storedToken;
      }
      return null;
    } catch {
      return null;
    }
  };

  const _loadRefreshToken = () => {
    try {
      const storedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
      if (storedRefreshToken) {
        refreshTokenValue.value = storedRefreshToken;
        return storedRefreshToken;
      }
      return null;
    } catch {
      return null;
    }
  };

  const _clearToken = () => {
    try {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      token.value = null;
    } catch {
      // Ignora erro de persistência
    }
  };

  const _clearRefreshToken = () => {
    try {
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      refreshTokenValue.value = null;
    } catch {
      // Ignora erro de persistência
    }
  };

  const _saveUserData = (userData) => {
    try {
      if (userData) {
        user.value = userData;
        userType.value = _normalizeUserType(userData?.user_type || userData?.type);
      }
    } catch {
      // Ignora erro ao salvar dados
    }
  };

  const _fetchCurrentUser = async () => {
    const { default: api } = await import('@/services/api');
    const response = await api.get('/auth/me/');
    _saveUserData(response.data);
    return response.data;
  };

  const _hydrateAuthStateFromResponse = (responseData) => {
    const accessToken = responseData?.access || null;
    const refreshToken = responseData?.refresh || null;
    const userData = responseData?.user || null;

    if (!accessToken) {
      throw new Error('Token de acesso não recebido do servidor');
    }

    _saveToken(accessToken);

    if (refreshToken) {
      _saveRefreshToken(refreshToken);
    }

    if (userData) {
      _saveUserData(userData);
    }

    return responseData;
  };

  // ===== PUBLIC ACTIONS =====

  const initializeAuth = async () => {
    try {
      const storedToken = _loadToken();
      const storedRefreshToken = _loadRefreshToken();

      if (!storedToken) {
        user.value = null;
        userType.value = null;
        return;
      }

      try {
        await _fetchCurrentUser();
      } catch (err) {
        if (storedRefreshToken) {
          await refreshToken();
          await _fetchCurrentUser();
          return;
        }

        throw err;
      }
    } catch {
      clearAuth();
    }
  };

  const login = async (email, password) => {
    const { default: api } = await import('@/services/api');
    const response = await api.post('/auth/login/', {
      email,
      password,
    });

    _hydrateAuthStateFromResponse(response.data);

    return response.data;
  };

  const signup = async (payload) => {
    const { default: api } = await import('@/services/api');
    const response = await api.post('/auth/signup/', payload);

    _hydrateAuthStateFromResponse(response.data);

    return response.data;
  };

  const checkEmail = async (email) => {
    const { default: api } = await import('@/services/api');
    const response = await api.post('/auth/check-email/', { email });
    return response.data;
  };

  const checkDocument = async (documento) => {
    const { default: api } = await import('@/services/api');
    const response = await api.post('/auth/check-document/', { documento });
    return response.data;
  };

  const logout = async () => {
    try {
      clearAuth();
    } catch {
      clearAuth();
    }
  };

  const clearAuth = () => {
    try {
      _clearToken();
      _clearRefreshToken();
      user.value = null;
      userType.value = null;

      window.dispatchEvent(new Event('logout'));
    } catch {
      // Ignora erro ao limpar sessão
    }
  };

  const setTokenFromStorage = (newToken, userData = null) => {
    if (newToken) {
      token.value = newToken;
      user.value = userData;
      userType.value = _normalizeUserType(userData?.user_type || userData?.type);
    } else {
      token.value = null;
      user.value = null;
      userType.value = null;
    }
  };

  const refreshToken = async () => {
    const storedRefreshToken = refreshTokenValue.value || _loadRefreshToken();

    if (!storedRefreshToken) {
      throw new Error('Refresh token não encontrado');
    }

    const { default: api } = await import('@/services/api');
    const response = await api.post('/auth/refresh/', {
      refresh: storedRefreshToken,
    });

    const newAccessToken = response.data?.access;
    if (!newAccessToken) {
      throw new Error('Novo access token não recebido');
    }

    _saveToken(newAccessToken);
    return newAccessToken;
  };

  // ===== SINCRONIZAÇÃO ENTRE ABAS =====
  if (typeof window !== 'undefined') {
    window.addEventListener('storage', (event) => {
      if (event.key === ACCESS_TOKEN_KEY) {
        if (!event.newValue) {
          setTokenFromStorage(null);
        } else {
          setTokenFromStorage(event.newValue);
          _fetchCurrentUser().catch(() => {
            // Ignora falha silenciosa de sincronização
          });
        }
      }

      if (event.key === REFRESH_TOKEN_KEY) {
        if (!event.newValue) {
          refreshTokenValue.value = null;
        } else {
          refreshTokenValue.value = event.newValue;
        }
      }
    });

    window.addEventListener('logout', () => {
      token.value = null;
      refreshTokenValue.value = null;
      user.value = null;
      userType.value = null;
    });
  }

  return {
    token,
    refreshTokenValue,
    user,
    userType,
    isLoggedIn,
    getCurrentUser,
    getToken,
    getCurrentUserType,
    initializeAuth,
    login,
    signup,
    checkEmail,
    checkDocument,
    logout,
    clearAuth,
    setTokenFromStorage,
    refreshToken,
  };
});
