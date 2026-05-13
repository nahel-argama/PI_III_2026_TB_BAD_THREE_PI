import axios from 'axios';

const externalApi = axios.create({
  baseURL: import.meta.env.VITE_EXTERNAL_PRODUCTS_HOST,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default externalApi;
