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
  } catch (err) {
    console.warn('Erro ao adicionar token no header:', err);
  }
  return config;
});

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
      const { response } = error;

      // Se não é erro 401, apenas re-lança (componente trata)
      if (!response || response.status !== 401) {
        return Promise.reject(error);
      }

      // ===== ERRO 401 CAPTURADO =====
      // Verifica se há token armazenado
      const token = localStorage.getItem('token');

      // Se NÃO há token → é um erro de credenciais inválidas (login)
      // Deixa o erro passar para o componente LoginView tratar
      if (!token) {
        console.warn('[API] 401 sem token (credenciais inválidas)', {
          url: response.config?.url,
        });
        return Promise.reject(error);
      }

      // Se HÁ token → é um erro real de autenticação (token expirado/inválido)
      // Faz logout automático
      console.warn('[API] 401 com token (autenticação expirada):', {
        url: response.config?.url,
        errorCode: response.data?.code,
        detail: response.data?.detail,
      });

      // Import dinâmico do auth store para evitar dependência circular
      const { useAuthStore } = await import('@/stores/auth');
      const authStore = useAuthStore();

      // ===== TODO: IMPLEMENTAR REFRESH TOKEN =====
      // Quando backend tiver endpoint POST /api/users/token/refresh/
      //
      // try {
      //   const newToken = await authStore.refreshToken();
      //   // Se sucesso, atualiza header e retenta requisição
      //   error.config.headers.Authorization = `Bearer ${newToken}`;
      //   return api(error.config);
      // } catch (refreshErr) {
      //   console.warn('[API] Falha ao renovar token:', refreshErr);
      //   authStore.clearAuth();
      //   return Promise.reject(error);
      // }

      // Por enquanto (sem refresh endpoint): logout imediato
      authStore.clearAuth();

      // Redireciona para login
      try {
        const { useRouter } = await import('vue-router');
        const router = useRouter();
        router.push('/login');
      } catch (routerErr) {
        console.warn('[API] Erro ao redirecionar via router, usando location.href:', routerErr);
        // Fallback: redireciona via location se router falhar
        window.location.href = '/login';
      }

      // Re-lança o erro para o componente decidir como exibir
      return Promise.reject(error);
    } catch (err) {
      console.error('[API] Erro ao processar erro 401:', err);
      return Promise.reject(error);
    }
  },
);

export default api;
