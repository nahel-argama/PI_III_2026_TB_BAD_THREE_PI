import api from './api';

function extractErrorMessage(error, fallbackMessage) {
  const data = error?.response?.data;

  if (typeof data === 'string' && data.trim()) {
    return data;
  }

  return (
    data?.error ||
    data?.detail ||
    data?.message ||
    data?.non_field_errors?.[0] ||
    fallbackMessage
  );
}

function buildOrdersServiceError(error, fallbackMessage) {
  const formattedError = new Error(extractErrorMessage(error, fallbackMessage));

  formattedError.name = 'OrdersServiceError';
  formattedError.status = error?.response?.status ?? null;
  formattedError.data = error?.response?.data ?? null;
  formattedError.response = error?.response;
  formattedError.cause = error;

  return formattedError;
}

export async function getPendingOrder(producerId) {
  try {
    const response = await api.get('/orders/', {
      params: {
        status: 'PENDING',
        producer: producerId,
      },
    });

    const payload = response.data;
    const orders = Array.isArray(payload) ? payload : payload?.results;

    if (!Array.isArray(orders) || orders.length === 0) {
      return null;
    }

    return orders[0];
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to get pending order.');
  }
}

export async function listPendingOrders(page = 1) {
  try {
    const response = await api.get('/orders/', {
      params: {
        status: 'PENDING',
        page,
      },
    });
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to list pending orders.');
  }
}

export async function listOrders(params = {}) {
  try {
    const response = await api.get('/orders/', { params });
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to list orders.');
  }
}

export async function createOrder(producerId) {
  try {
    const response = await api.post('/orders/', { producer: producerId });
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to create order.');
  }
}

export async function confirmOrder(orderId) {
  try {
    const response = await api.post(`/orders/${orderId}/confirm/`);
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to confirm order.');
  }
}

export async function cancelOrder(orderId) {
  try {
    const response = await api.post(`/orders/${orderId}/cancel/`);
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to cancel order.');
  }
}

export async function getOrder(orderId) {
  try {
    const response = await api.get(`/orders/${orderId}/`);
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to fetch order.');
  }
}

export async function addItemToOrder(orderId, productId, quantity) {
  try {
    const response = await api.post(`/orders/${orderId}/items/`, {
      product: productId,
      quantity,
    });
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to add item to order.');
  }
}

export async function updateItemQuantity(orderId, itemId, quantity) {
  try {
    const response = await api.patch(`/orders/${orderId}/items/${itemId}/`, {
      quantity,
    });
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to update order item quantity.');
  }
}

export async function removeItemFromOrder(orderId, itemId) {
  try {
    const response = await api.delete(`/orders/${orderId}/items/${itemId}/`);
    return response.data ?? null;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to remove item from order.');
  }
}

export async function deleteOrder(orderId) {
  try {
    const response = await api.delete(`/orders/${orderId}/`);
    return response.data ?? null;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Unable to delete order.');
  }
}

export async function payOrder(orderId, { payment_method, card }) {
  try {
    const payload = { payment_method };
    if (payment_method === 'credit_card' && card) {
      payload.card = card;
    }
    const response = await api.post(`/orders/${orderId}/pay/`, payload);
    return response.data;
  } catch (error) {
    throw buildOrdersServiceError(error, 'Não foi possível processar o pagamento.');
  }
}
