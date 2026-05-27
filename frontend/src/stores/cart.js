import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import {
  addItemToOrder,
  confirmOrder as confirmOrderRequest,
  createOrder,
  getOrder,
  getPendingOrder,
  listPendingOrders,
  removeItemFromOrder,
  updateItemQuantity,
} from '@/services/ordersService';

function getProducerIdFromProduct(product) {
  if (!product || typeof product !== 'object') {
    return null;
  }

  const producer = product.producer;

  if (typeof producer === 'number' || typeof producer === 'string') {
    return Number(producer);
  }

  if (producer && typeof producer === 'object') {
    return Number(producer.id ?? producer.pk ?? producer.value ?? NaN);
  }

  return Number(product.producer_id ?? product.producerId ?? NaN);
}

function getProducerIdFromOrder(order) {
  if (!order || typeof order !== 'object') {
    return null;
  }

  const producer = order.producer;

  if (typeof producer === 'number' || typeof producer === 'string') {
    return Number(producer);
  }

  if (producer && typeof producer === 'object') {
    return Number(producer.id ?? producer.pk ?? producer.value ?? NaN);
  }

  return null;
}

function hasOrderItems(order) {
  return Array.isArray(order?.items) && order.items.length > 0;
}

function normalizeCartError(error, fallbackMessage) {
  const data = error?.data ?? error?.response?.data ?? null;
  const message =
    error?.message ||
    data?.error ||
    data?.detail ||
    data?.message ||
    data?.non_field_errors?.[0] ||
    fallbackMessage;

  const formattedError = new Error(message);
  formattedError.name = 'CartStoreError';
  formattedError.status = error?.status ?? error?.response?.status ?? null;
  formattedError.data = data;
  formattedError.cause = error;
  return formattedError;
}

function isDuplicatePendingOrderError(error) {
  const message = String(error?.message || '').toLowerCase();
  return message.includes('already a pending order for this producer');
}

function isNotFoundError(error) {
  return Number(error?.status ?? error?.response?.status) === 404;
}

export const useCartStore = defineStore('cart', () => {
  const pendingOrders = ref({});
  const isLoading = ref(false);
  const error = ref(null);

  const pendingOrdersList = computed(() => Object.values(pendingOrders.value));

  const getPendingOrderByProducer = (producerId) => {
    const key = String(producerId);
    return pendingOrders.value[key] ?? null;
  };

  const getPendingOrderById = (orderId) => {
    for (const order of pendingOrdersList.value) {
      if (Number(order?.id) === Number(orderId)) {
        return order;
      }
    }
    return null;
  };

  const clearError = () => {
    error.value = null;
  };

  const setPendingOrder = (order) => {
    const producerId = getProducerIdFromOrder(order);
    if (!producerId || Number.isNaN(producerId)) {
      return;
    }

    const key = String(producerId);

    if (order?.status === 'PENDING' && hasOrderItems(order)) {
      pendingOrders.value[key] = order;
      return;
    }

    delete pendingOrders.value[key];
  };

  const removePendingOrderByProducer = (producerId) => {
    const key = String(producerId);
    if (pendingOrders.value[key]) {
      delete pendingOrders.value[key];
    }
  };

  const refreshOrder = async (orderId) => {
    const refreshedOrder = await getOrder(orderId);
    setPendingOrder(refreshedOrder);
    return refreshedOrder;
  };

  const ensurePendingOrder = async (producerId) => {
    const localOrder = getPendingOrderByProducer(producerId);
    if (localOrder && localOrder.status === 'PENDING') {
      return localOrder;
    }

    const pendingFromApi = await getPendingOrder(producerId);
    if (pendingFromApi) {
      setPendingOrder(pendingFromApi);
      return pendingFromApi;
    }

    try {
      const createdOrder = await createOrder(producerId);
      setPendingOrder(createdOrder);
      return createdOrder;
    } catch (createError) {
      // Race condition safety: another request/device created pending order first.
      if (!isDuplicatePendingOrderError(createError)) {
        throw createError;
      }

      const existingOrder = await getPendingOrder(producerId);
      if (!existingOrder) {
        throw createError;
      }

      setPendingOrder(existingOrder);
      return existingOrder;
    }
  };

  const addProductToCart = async (product, quantity) => {
    isLoading.value = true;
    clearError();

    try {
      const producerId = getProducerIdFromProduct(product);
      if (!producerId || Number.isNaN(producerId)) {
        throw new Error('Invalid producer on selected product.');
      }

      const productId = Number(product?.id);
      if (!productId || Number.isNaN(productId)) {
        throw new Error('Invalid product id.');
      }

      const parsedQuantity = Number(quantity);
      if (!parsedQuantity || parsedQuantity <= 0) {
        throw new Error('Quantity must be greater than zero.');
      }

      const order = await ensurePendingOrder(producerId);
      await addItemToOrder(order.id, productId, parsedQuantity);

      return await refreshOrder(order.id);
    } catch (requestError) {
      const formattedError = normalizeCartError(requestError, 'Unable to add product to cart.');
      error.value = formattedError;
      throw formattedError;
    } finally {
      isLoading.value = false;
    }
  };

  const updateItem = async (orderId, itemId, newQuantity) => {
    isLoading.value = true;
    clearError();

    try {
      const quantity = Number(newQuantity);
      if (!quantity || quantity <= 0) {
        throw new Error('Quantity must be greater than zero.');
      }

      await updateItemQuantity(orderId, itemId, quantity);
      return await refreshOrder(orderId);
    } catch (requestError) {
      const formattedError = normalizeCartError(requestError, 'Unable to update item.');
      error.value = formattedError;
      throw formattedError;
    } finally {
      isLoading.value = false;
    }
  };

  const removeItem = async (orderId, itemId) => {
    isLoading.value = true;
    clearError();

    try {
      const orderBeforeRemoval = getPendingOrderById(orderId);
      const producerId = getProducerIdFromOrder(orderBeforeRemoval);

      await removeItemFromOrder(orderId, itemId);

      try {
        return await refreshOrder(orderId);
      } catch (refreshError) {
        if (!isNotFoundError(refreshError)) {
          throw refreshError;
        }

        if (producerId) {
          removePendingOrderByProducer(producerId);
        }

        return null;
      }
    } catch (requestError) {
      const formattedError = normalizeCartError(requestError, 'Unable to remove item.');
      error.value = formattedError;
      throw formattedError;
    } finally {
      isLoading.value = false;
    }
  };

  const confirmOrder = async (orderId) => {
    isLoading.value = true;
    clearError();

    try {
      const confirmedOrder = await confirmOrderRequest(orderId);
      setPendingOrder(confirmedOrder);
      return confirmedOrder;
    } catch (requestError) {
      const formattedError = normalizeCartError(requestError, 'Unable to confirm order.');
      error.value = formattedError;
      throw formattedError;
    } finally {
      isLoading.value = false;
    }
  };

  const syncPendingOrders = async () => {
    isLoading.value = true;
    clearError();

    try {
      const nextPendingOrders = {};
      let currentPage = 1;
      let hasNextPage = true;

      while (hasNextPage) {
        const payload = await listPendingOrders(currentPage);
        const pageOrders = Array.isArray(payload) ? payload : (payload?.results ?? []);

        for (const order of pageOrders) {
          if (order?.status !== 'PENDING' || !hasOrderItems(order)) {
            continue;
          }

          const producerId = getProducerIdFromOrder(order);
          if (!producerId || Number.isNaN(producerId)) {
            continue;
          }

          nextPendingOrders[String(producerId)] = order;
        }

        if (Array.isArray(payload)) {
          hasNextPage = false;
          continue;
        }

        hasNextPage = Boolean(payload?.next);
        currentPage += 1;
      }

      pendingOrders.value = nextPendingOrders;
      return pendingOrdersList.value;
    } catch (requestError) {
      const formattedError = normalizeCartError(requestError, 'Unable to sync pending orders.');
      error.value = formattedError;
      throw formattedError;
    } finally {
      isLoading.value = false;
    }
  };

  const clearCartState = () => {
    pendingOrders.value = {};
    clearError();
  };

  return {
    pendingOrders,
    pendingOrdersList,
    isLoading,
    error,
    addProductToCart,
    updateItem,
    removeItem,
    confirmOrder,
    syncPendingOrders,
    getPendingOrderByProducer,
    getPendingOrderById,
    setPendingOrder,
    removePendingOrderByProducer,
    clearCartState,
    clearError,
  };
});
