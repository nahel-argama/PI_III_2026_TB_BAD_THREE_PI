import api from './api';

/**
 * Adiciona um produto à wishlist do usuário.
 * 
 * @param {string|number} productId - O ID externo do produto.
 * @returns {Promise<Object>} O item da wishlist criado.
 */
export async function addProductToWishlist(productId) {
  const payload = {
    product_external_key: String(productId),
  };

  const response = await api.post('/wishlists/items/', payload);
  return response.data;
}

/**
 * Remove um produto da wishlist do usuário.
 * 
 * @param {number} itemId - O ID do item na wishlist (ID interno).
 * @returns {Promise<void>}
 */
export async function removeProductFromWishlist(itemId) {
  await api.delete(`/wishlists/items/${itemId}/`);
}

/**
 * Lista todos os itens da wishlist do usuário com suporte a paginação e busca.
 * 
 * @param {Object} params - Parâmetros de busca.
 * @param {number} params.page - Número da página.
 * @param {string} [params.productName] - Termo de busca por nome do produto.
 * @returns {Promise<Object>} Resposta paginada com a lista de itens.
 */
export async function listWishlistItems({ page = 1, productName = '' } = {}) {
  const params = { page };
  if (productName) {
    params.product_name = productName;
  }
  
  const response = await api.get('/wishlists/items/', { params });
  return response.data;
}
