import api from './api';

/**
 * Retorna os dados do perfil do usuário autenticado.
 *
 * Endpoint: GET /api/auth/me/
 *
 * @returns {Promise<Object>} Dados do usuário: id, name, email, user_type, profile, address.
 */
export async function fetchCurrentUserProfile() {
  const response = await api.get('/auth/me/');
  return response.data;
}
