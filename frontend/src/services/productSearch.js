import externalApi from './externalApi';

export const productSearchService = {
  /**
   * Busca produtos no serviço externo.
   *
   * @param {string} query - Termo de busca.
   * @returns {Promise<Array>} Lista de produtos encontrados.
   */
  async search(query) {
    try {
      // O backend espera o termo entre aspas, ex: "laranja"
      const response = await externalApi.get('/api/products/search', {
        params: { query: `"${query}"` },
      });
      return response.data;
    } catch (error) {
      console.error('[ProductSearchService] Erro ao buscar produtos:', error);
      throw error;
    }
  },
};
