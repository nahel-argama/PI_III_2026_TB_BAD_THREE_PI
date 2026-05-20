import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * ===== INTERCEPTOR DE REQUEST =====
 *
 * Adiciona o token JWT no header Authorization de toda requisição
 * que tenha um token armazenado no localStorage.
 *
 * Formato: Authorization: Bearer <token>
 */
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch {
    // Ignora erro ao obter do localStorage
  }
  return config;
});

const isAuthEndpoint = (url = '') => {
  return /\/auth\/(login|signup|refresh|verify|check-email|check-document)\//.test(url);
};

/**
 * ===== INTERCEPTOR DE RESPOSTA =====
 *
 * Captura erros 401 (token inválido/expirado) e executa logout automático.
 *
 * Comportamento:
 * 1. Se status === 401 E há token armazenado → token está inválido/expirado
 *    → Faz logout automático e redireciona para /login
 * 2. Se status === 401 E NÃO há token → credenciais inválidas no login
 *    → Deixa o erro passar para o componente tratar
 * 3. Outros erros → apenas re-lança (componente trata)
 *
 * Erros que retornam 401 (SimpleJWT):
 * - Token expirado: precisa logout automático
 * - Token inválido: precisa logout automático
 * - Credenciais inválidas (login): deixa passar para componente mostrar erro
 */
api.interceptors.response.use(
  // Sucesso - apenas passa adiante
  (response) => response,

  // Erro - captura 401 inteligentemente
  async (error) => {
    try {
      const { response, config } = error;

      // Se não é erro 401, apenas re-lança (componente trata)
      if (!response || response.status !== 401) {
        return Promise.reject(error);
      }

      if (config?._retry) {
        return Promise.reject(error);
      }

      if (isAuthEndpoint(config?.url)) {
        return Promise.reject(error);
      }

      // ===== ERRO 401 CAPTURADO =====
      // Verifica se há token armazenado
      const token = localStorage.getItem('token');
      const refreshToken = localStorage.getItem('refresh_token');

      // Se NÃO há token → é um erro de credenciais inválidas (login)
      // Deixa o erro passar para o componente LoginView tratar
      if (!token && !refreshToken) {
        return Promise.reject(error);
      }

      // Import dinâmico do auth store para evitar dependência circular
      const { useAuthStore } = await import('@/stores/auth');
      const authStore = useAuthStore();

      if (refreshToken) {
        try {
          const newToken = await authStore.refreshToken();
          config._retry = true;
          config.headers.Authorization = `Bearer ${newToken}`;
          return api(config);
        } catch {
          // Ignora falha de renovação do token
        }
      }

      authStore.clearAuth();

      try {
        window.location.href = '/login';
      } catch {
        // Ignora erro de redirecionamento
      }

      // Re-lança o erro para o componente decidir como exibir
      return Promise.reject(error);
    } catch {
      return Promise.reject(error);
    }
  },
);

export default api;
