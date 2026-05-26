import paymentGatewayApi from './paymentGatewayApi';

/**
 * Mapeamento de IDs de método de pagamento (frontend) para os valores
 * aceitos pelo PI Payment Gateway.
 *
 * @type {Record<number, string>}
 */
const PAYMENT_METHOD_MAP = {
  1: 'pix',
  2: 'invoice',
  3: 'credit_card',
};

/**
 * Constrói e lança um erro padronizado de gateway de pagamento.
 *
 * @param {string} message
 * @param {number|null} httpStatus
 * @param {Array} errors
 * @param {unknown} cause
 * @returns {never}
 */
function buildPaymentGatewayError(message, httpStatus = null, errors = [], cause = null) {
  const error = new Error(message);
  error.name = 'PaymentGatewayError';
  error.status = httpStatus;
  error.errors = errors;
  error.cause = cause;
  throw error;
}

/**
 * Processa um pagamento no PI Payment Gateway.
 *
 * @param {object} params
 * @param {number} params.selectedPaymentId - ID do método de pagamento selecionado no frontend
 *   (1 = pix, 2 = invoice, 3 = credit_card)
 * @param {number} params.price - Valor total do pedido (deve ser > 0)
 * @param {object} [params.card] - Dados do cartão. Obrigatório apenas quando selectedPaymentId === 3
 * @param {string} params.card.holder_name
 * @param {string} params.card.number
 * @param {number} params.card.expiry_month
 * @param {number} params.card.expiry_year
 * @param {string} params.card.cvv
 *
 * @returns {Promise<{ status: 'success', created_at: string }>}
 *
 * @throws {Error} PaymentGatewayError — quando o gateway rejeita o pagamento (HTTP 402 ou 422)
 * @throws {Error} PaymentGatewayError — quando ocorre erro de rede ou timeout
 */
export async function processPayment({ selectedPaymentId, price, card }) {
  const paymentMethod = PAYMENT_METHOD_MAP[selectedPaymentId];

  if (!paymentMethod) {
    buildPaymentGatewayError(
      `Método de pagamento inválido: ${selectedPaymentId}`,
      null,
      [],
    );
  }

  const payload = {
    price,
    payment_method: paymentMethod,
  };

  if (paymentMethod === 'credit_card') {
    if (!card) {
      buildPaymentGatewayError(
        'Dados do cartão são obrigatórios para pagamento com cartão de crédito.',
        null,
        [],
      );
    }
    payload.card = card;
  }

  try {
    const response = await paymentGatewayApi.post('/payments', payload);
    return response.data;
  } catch (error) {
    const httpStatus = error?.response?.status ?? null;
    const data = error?.response?.data;

    // HTTP 402 — regras de negócio do cartão falharam
    // HTTP 422 — payload malformado
    if (httpStatus === 402 || httpStatus === 422) {
      const message =
        data?.message || data?.detail?.message || (typeof data?.detail === 'string' ? data.detail : null) || 'Pagamento recusado pelo gateway.';
      const errors = Array.isArray(data?.errors) ? data.errors : [];

      buildPaymentGatewayError(message, httpStatus, errors, error);
    }

    // Erro de rede, timeout ou status inesperado
    buildPaymentGatewayError(
      'Não foi possível conectar ao serviço de pagamento. Tente novamente.',
      httpStatus,
      [],
      error,
    );
  }
}
