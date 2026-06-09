import api from './api';

export async function listProducts(params = {}) {
  const response = await api.get('/products/', {
    params: {
      is_active: true,
      ...params,
    },
  });
  return response.data;
}

export async function createProduct(data) {
  const response = await api.post('/products/', data);
  return response.data;
}

export async function deleteProduct(id) {
  const response = await api.patch(`/products/${id}/`, { is_active: false });
  return response.data;
}

export async function getProductById(id) {
  const response = await api.get(`/products/${id}/`);
  return response.data;
}

export async function generateProductDescription(productName) {
  const response = await api.post('/products/generate/description/', { product_name: productName });
  return response.data;
}
