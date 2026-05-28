import api from '@/services/api';

export const wishlistAnalyticsService = {
  /**
   * Fetch top products from wishlist
   * @param {Object} params - Query parameters
   * @param {string} [params.state] - State abbreviation (e.g., 'SP')
   * @param {number} [params.top] - Number of top items to fetch (e.g., 5, 10)
   * @returns {Promise<Object>} The API response
   */
  async getTopProducts(params) {
    const response = await api.get('/wishlists/top-products/', { params });
    return response.data;
  },
};
