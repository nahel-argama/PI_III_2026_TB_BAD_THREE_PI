/**
 * Checkout Mock Data and Utilities
 * Contains initial mock data and helper functions for checkout calculations
 */

/**
 * Initial mock order items
 * @type {import('./checkout').OrderItem[]}
 */
export const initialOrderItems = [
  {
    id: 1,
    name: 'Tomate Carmem',
    producer: 'Fazenda Sol Nascente',
    image: `https://picsum.photos/80/80?random=${Math.random()}`,
    quantity: 150,
    pricePerKg: 3.5,
    distance: 45,
    inStock: true,
  },
  {
    id: 2,
    name: 'Alface Crespa',
    producer: 'Sítio Verde Vale',
    image: `https://picsum.photos/80/80?random=${Math.random()}`,
    quantity: 50,
    pricePerKg: 2.0,
    distance: 20,
    inStock: true,
  },
];

/**
 * Initial mock producer
 * @type {import('./checkout').Producer}
 */
export const initialProducer = {
  id: 1,
  name: 'Fazenda Sol Nascente',
  location: 'Mogi das Cruzes - SP',
  distance: 45,
  trusted: true,
};

/**
 * Default platform fee percentage (5%)
 */
export const DEFAULT_PLATFORM_FEE_PERCENT = 5;

/**
 * Calculate subtotal from order items
 * @param {import('./checkout').OrderItem[]} items - Array of order items
 * @returns {number} Subtotal in currency (quantity * pricePerKg for each item)
 */
export function calculateSubtotal(items) {
  return items.reduce((sum, item) => sum + item.quantity * item.pricePerKg, 0);
}

/**
 * Calculate platform fee based on percentage
 * @param {number} subtotal - Subtotal amount
 * @param {number} [percent=5] - Platform fee percentage (default 5%)
 * @returns {number} Platform fee amount
 */
export function calculatePlatformFee(subtotal, percent = DEFAULT_PLATFORM_FEE_PERCENT) {
  return (subtotal * percent) / 100;
}

/**
 * Calculate total amount
 * @param {number} subtotal - Subtotal amount
 * @param {number} platformFee - Platform fee amount
 * @returns {number} Total = subtotal + platformFee
 */
export function calculateTotal(subtotal, platformFee) {
  return subtotal + platformFee;
}

/**
 * Create initial checkout state with mock data
 * @returns {import('./checkout').CheckoutState} Complete checkout state object
 */
export function createInitialCheckoutState() {
  return {
    items: initialOrderItems,
    producer: initialProducer,
    selectedPaymentId: 1, // Pix by default
    platformFeePercent: DEFAULT_PLATFORM_FEE_PERCENT,
  };
}
