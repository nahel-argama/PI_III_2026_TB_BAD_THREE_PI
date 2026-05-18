import axios from 'axios';

const brasilApi = axios.create({
  baseURL: 'https://brasilapi.com.br/api',
});

export const fetchAddressByCep = async (cep) => {
  const response = await brasilApi.get(`/cep/v1/${cep}`);
  return response.data;
};

export const fetchStates = async () => {
  const response = await brasilApi.get('/ibge/uf/v1');
  return response.data;
};

export default {
  fetchAddressByCep,
  fetchStates,
};
