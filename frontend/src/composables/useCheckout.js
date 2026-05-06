/**
 * Checkout Composable
 * Manages all checkout state and calculations
 */

import { ref, computed } from 'vue';
import {
  createInitialCheckoutState,
  calculateSubtotal,
  calculatePlatformFee,
  calculateTotal,
} from '@/data/checkoutData';

/**
 * Composable for managing checkout state and data
 * @returns {Object} Checkout state, computed values, and methods
 */
export function useCheckout() {
  // Initialize state
  const initialState = createInitialCheckoutState();
  const state = ref(initialState);

  // Computed properties for reactive calculations
  const items = computed(() => state.value.items);
  const producer = computed(() => state.value.producer);
  const selectedPaymentId = computed(() => state.value.selectedPaymentId);

  /**
   * Calculate subtotal from current items
   */
  const subtotal = computed(() => calculateSubtotal(items.value));

  /**
   * Calculate platform fee based on current subtotal
   */
  const platformFee = computed(() =>
    calculatePlatformFee(subtotal.value, state.value.platformFeePercent),
  );

  /**
   * Calculate total (subtotal + platform fee)
   */
  const total = computed(() => calculateTotal(subtotal.value, platformFee.value));

  /**
   * Calculate line item total (quantity * pricePerKg) for a specific item
   * @param {Object} item - Order item
   * @returns {number}
   */
  const getItemTotal = (item) => item.quantity * item.pricePerKg;

  /**
   * Select a payment method
   * @param {number} paymentId - ID of the payment method to select
   */
  const selectPaymentMethod = (paymentId) => {
    state.value.selectedPaymentId = paymentId;
  };

  /**
   * Update order items
   * @param {Object[]} newItems - New array of order items
   */
  const setItems = (newItems) => {
    state.value.items = newItems;
  };

  /**
   * Update producer
   * @param {Object} newProducer - New producer object
   */
  const setProducer = (newProducer) => {
    state.value.producer = newProducer;
  };

  /**
   * Load checkout state from external source (e.g., API)
   * @param {Partial<import('@/types/checkout').CheckoutState>} newState - Complete checkout state to load
   */
  const loadCheckoutState = (newState) => {
    state.value = {
      ...state.value,
      ...newState,
    };
  };

  return {
    // State
    state,
    items,
    producer,
    selectedPaymentId,

    // Computed values
    subtotal,
    platformFee,
    total,

    // Methods
    getItemTotal,
    selectPaymentMethod,
    setItems,
    setProducer,
    loadCheckoutState,
  };
}
