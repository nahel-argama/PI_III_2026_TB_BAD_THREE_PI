import api from './api';

export async function listCategories() {
  const response = await api.get('/categories/');
  return response.data;
}
