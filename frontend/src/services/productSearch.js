import externalApi from './externalApi';
import { capitalize } from '@/utils/string';

export const productSearchService = {
  /**
   * Busca produtos no serviço externo.
   *
   * @param {string} query - Termo de busca.
   * @returns {Promise<Array>} Lista de produtos encontrados.
   */
  async search(query) {
    const response = await externalApi.get('/api/products/search', {
      params: { query: query || '' },
    });

    if (Array.isArray(response.data)) {
      return response.data.map((item) => ({
        ...item,
        name: item.name ? capitalize(item.name) : '',
      }));
    }

    return response.data;
  },
};
