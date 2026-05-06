/**
 * Checkout Module Types (JSDoc)
 * Defines all type definitions for the checkout flow
 * @typedef {Object} OrderItem
 * @property {number} id
 * @property {string} name
 * @property {string} producer
 * @property {string} image
 * @property {number} quantity - in kg
 * @property {number} pricePerKg
 * @property {number} distance - in km
 * @property {boolean} inStock
 *
 * @typedef {Object} Producer
 * @property {number} id
 * @property {string} name
 * @property {string} location
 * @property {number} distance - in km
 * @property {boolean} trusted
 *
 * @typedef {Object} PaymentMethod
 * @property {number} id
 * @property {string} name
 * @property {string} description
 * @property {string} [icon]
 *
 * @typedef {Object} CheckoutState
 * @property {OrderItem[]} items
 * @property {Producer[]} producers
 * @property {PaymentMethod[]} paymentMethods
 * @property {number} selectedPaymentId
 * @property {number} platformFeePercent
 */

export {};
