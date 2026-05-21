import api from './api';

export async function listProducts(params = {}) {
  const response = await api.get('/products/', { params });
  return response.data;
}
