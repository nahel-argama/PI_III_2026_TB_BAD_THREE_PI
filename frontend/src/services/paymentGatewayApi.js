import axios from 'axios';

const paymentGatewayApi = axios.create({
  baseURL: import.meta.env.VITE_PAYMENT_GATEWAY_URL || 'http://localhost:8002',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default paymentGatewayApi;
