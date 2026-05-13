import axios from 'axios';

const brasilApi = axios.create({
  baseURL: 'https://brasilapi.com.br/api',
});

export const fetchAddressByCep = async (cep) => {
  try {
    const response = await brasilApi.get(`/cep/v1/${cep}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar CEP:', error);
    throw error;
  }
};

export const fetchStates = async () => {
  try {
    const response = await brasilApi.get('/ibge/uf/v1');
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar estados:', error);
    throw error;
  }
};

export default {
  fetchAddressByCep,
  fetchStates,
};
