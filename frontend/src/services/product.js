import api from './api';

export async function listProducts(params = {}) {
  const response = await api.get('/products/', { params });
  return response.data;
}

export async function createProduct(data) {
  const response = await api.post('/products/', data);
  return response.data;
}

export async function deleteProduct(id) {
  const response = await api.delete(`/products/${id}/`);
  return response.data;
}

export async function getProductById(id) {
  const response = await api.get(`/products/${id}/`);
  return response.data;
}
