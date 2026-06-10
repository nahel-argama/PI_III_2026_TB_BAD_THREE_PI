<template>
  <div class="checkout-container min-h-screen bg-white">
    <CheckoutHeader @cancel="isCancelDialogOpen = true" />

    <div class="bg-white py-12">
      <div class="container mx-auto px-6">
        <div
          v-if="pageError"
          class="mx-auto max-w-3xl rounded-2xl border border-rose-200 bg-rose-50 p-6"
        >
          <h2 class="text-lg font-black text-rose-800">Checkout indisponível</h2>
          <p class="mt-2 text-sm text-rose-700">{{ pageError }}</p>
          <button
            type="button"
            class="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-sm font-bold text-white transition hover:bg-slate-700"
            @click="goToDashboard"
          >
            Voltar ao painel
          </button>
        </div>

        <div
          v-else-if="isLoading"
          class="rounded-2xl border border-slate-200 bg-white p-8 text-center"
        >
          <p class="text-sm font-semibold text-slate-700">Carregando pedido...</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-3 lg:gap-8">
          <div class="space-y-6 lg:col-span-2">
            <div
              v-if="isReadOnly"
              class="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm font-semibold text-amber-800"
            >
              Pedido não editável. Status atual: {{ order?.status || 'DESCONHECIDO' }}.
            </div>

            <CheckoutOrderSummary :items="checkoutItems" />
            <CheckoutProducersInfo
              :producer="checkoutProducer"
              :order-status="order?.status || null"
            />
            <CheckoutDelivery />
          </div>

          <div class="lg:sticky lg:top-24 lg:h-fit">
            <div class="space-y-6">
              <CheckoutValuesSummary
                :subtotal="subtotal"
                :platform-fee="platformFee"
                :total="total"
              />
              <CheckoutPayment
                :selected-payment-id="selectedPaymentId"
                :pix="true"
                :boleto="true"
                :credit-card="true"
                :disabled="isReadOnly || isConfirming"
                :on-select-payment-method="selectPaymentMethod"
              />
              <CheckoutFooter
                :disabled="isReadOnly || isConfirming || !hasItems"
                :loading="isConfirming"
                :readonly="isReadOnly"
                :has-items="hasItems"
                @confirm="handleConfirmOrder"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <AppDialog
      v-model="isCancelDialogOpen"
      variant="danger"
      title="Descartar pedido?"
      message="Ao voltar, este pedido será descartado e os itens serão removidos do seu carrinho. Deseja continuar?"
      confirm-label="Sim, descartar pedido"
      cancel-label="Não, continuar compra"
      :show-cancel="true"
      @confirm="executeCancelOrder"
    />

    <CreditCardModal
      v-model="isCreditCardModalOpen"
      :disabled="isConfirming"
      @confirm="onCreditCardConfirm"
      @cancel="isCreditCardModalOpen = false"
    />

    <PaymentConfirmationModal
      ref="paymentModalRef"
      v-model="isPaymentModalOpen"
      :amount="formattedTotal"
      :payment-method="paymentMethodLabel"
      :error-message="
        paymentModalError || 'Ocorreu um erro ao processar seu pagamento. O pedido foi cancelado.'
      "
      :cancel-label="selectedPaymentId === 3 ? 'Voltar' : 'Cancelar'"
      :closable="!isConfirming"
      :persistent="isConfirming"
      :auto-close="true"
      :auto-close-delay="3000"
      size="md"
      @confirm="onPaymentModalConfirm"
      @success="onPaymentModalSuccess"
      @close="onPaymentModalClose"
      @retry="onPaymentModalClose"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CheckoutHeader from '@/components/checkout/CheckoutHeader.vue';
import CheckoutOrderSummary from '@/components/checkout/CheckoutOrderSummary.vue';
import CheckoutProducersInfo from '@/components/checkout/CheckoutProducersInfo.vue';
import CheckoutPayment from '@/components/checkout/CheckoutPayment.vue';
import CheckoutDelivery from '@/components/checkout/CheckoutDelivery.vue';
import CheckoutValuesSummary from '@/components/checkout/CheckoutValuesSummary.vue';
import CheckoutFooter from '@/components/checkout/CheckoutFooter.vue';
import AppDialog from '@/components/ui/AppDialog.vue';
import CreditCardModal from '@/components/checkout/CreditCardModal.vue';
import PaymentConfirmationModal from '@/components/checkout/PaymentConfirmationModal.vue';
import { getOrder, deleteOrder as deleteOrderApi, payOrder } from '@/services/ordersService';
import { useCartStore } from '@/stores/cart';
import { useToast } from '@/composables/useToast';

const route = useRoute();
const router = useRouter();
const cartStore = useCartStore();
const toast = useToast();

const order = ref(null);
const isLoading = ref(false);
const isConfirming = ref(false);
const pageError = ref('');
const selectedPaymentId = ref(1);
const isCancelDialogOpen = ref(false);
const isCreditCardModalOpen = ref(false);
const isPaymentModalOpen = ref(false);
const pendingCardData = ref(null);
const paymentModalError = ref('');

const orderId = computed(() => {
  const rawValue = route.query.order_id;
  const parsed = Number(rawValue);
  if (!parsed || Number.isNaN(parsed)) {
    return null;
  }
  return parsed;
});

const checkoutItems = computed(() => {
  const items = Array.isArray(order.value?.items) ? order.value.items : [];
  return items.map((item) => {
    const productData = item?.product_data || {};
    const unitPrice = Number(item?.unit_price || 0);

    return {
      id: item.id,
      name: productData.name || `Produto #${item.product}`,
      productId: item.product,
      quantity: Number(item.quantity || 0),
      pricePerKg: unitPrice,
      lineTotal: Number(item.quantity || 0) * unitPrice,
      imageUrl: productData.images?.[0]?.image || null,
    };
  });
});

const checkoutProducer = computed(() => {
  const data = order.value?.producer_data;
  if (data) {
    return {
      ...data,
      name: data.trade_name || data.name || `Produtor #${data.id}`,
    };
  }
  const producer = order.value?.producer;
  return {
    id: producer,
    name: `Produtor #${producer ?? '-'}`,
  };
});

const hasItems = computed(() => checkoutItems.value.length > 0);
const isPending = computed(() => order.value?.status === 'PENDING');
const isReadOnly = computed(() => !isPending.value || !hasItems.value);

const subtotal = computed(() => {
  const apiSub = Number(order.value?.subtotal_value || 0);
  if (apiSub > 0) return apiSub;
  return checkoutItems.value.reduce((sum, item) => sum + Number(item.lineTotal || 0), 0);
});

const platformFee = computed(() => {
  const apiFee = Number(order.value?.fee_value || 0);
  if (apiFee > 0) return apiFee;
  return subtotal.value * 0.05;
});

const total = computed(() => {
  const apiTotal = Number(order.value?.total_value || 0);
  if (apiTotal > 0) {
    return apiTotal;
  }
  return subtotal.value + platformFee.value;
});

const PAYMENT_METHOD_LABELS = { 1: 'PIX', 2: 'Boleto Bancário', 3: 'Cartão de Crédito' };

const formattedTotal = computed(() => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(total.value);
});

const paymentMethodLabel = computed(
  () => PAYMENT_METHOD_LABELS[selectedPaymentId.value] ?? 'Desconhecido',
);

function selectPaymentMethod(paymentId) {
  selectedPaymentId.value = paymentId;
}

function goToDashboard() {
  router.push('/dashboard');
}

async function loadOrder() {
  if (!orderId.value) {
    order.value = null;
    pageError.value = 'Pedido inválido. Selecione um pedido pendente no carrinho.';
    return;
  }

  isLoading.value = true;
  pageError.value = '';
  order.value = null;

  try {
    const fetchedOrder = await getOrder(orderId.value);
    order.value = fetchedOrder;
    cartStore.setPendingOrder(fetchedOrder);
  } catch (error) {
    pageError.value = error?.message || 'Não foi possível carregar o pedido.';
  } finally {
    isLoading.value = false;
  }
}

// Chamado quando o usuário clica "Confirmar pagamento" no PaymentConfirmationModal
const paymentModalRef = ref(null);

const PAYMENT_METHOD_MAP = { 1: 'pix', 2: 'invoice', 3: 'credit_card' };

async function onPaymentModalConfirm() {
  isConfirming.value = true;
  paymentModalError.value = '';

  const payment_method = PAYMENT_METHOD_MAP[selectedPaymentId.value];

  try {
    // ÚNICA chamada: o backend chama o gateway e confirma/cancela internamente
    const confirmedOrder = await payOrder(orderId.value, {
      payment_method,
      card: selectedPaymentId.value === 3 ? pendingCardData.value : null,
    });

    order.value = confirmedOrder;
    const producerId = checkoutProducer.value?.id;
    if (producerId) cartStore.removePendingOrderByProducer(producerId);

    paymentModalRef.value?.setState('success');
    toast.success('Pedido confirmado com sucesso.', 'Compra finalizada');
  } catch (error) {
    // Se o backend retornou 402 ou 422 (gateway rejeitou): pedido já foi cancelado pelo backend
    if (error.status === 402 || error.status === 422) {
      const producerId = checkoutProducer.value?.id;
      if (producerId) cartStore.removePendingOrderByProducer(producerId);
      paymentModalError.value = error.message || 'Pagamento recusado.';
    } else if (error.status === 503) {
      // Gateway indisponível: pedido ainda PENDING, usuário pode tentar novamente
      paymentModalError.value = error.message || 'Serviço de pagamento indisponível.';
      // NÃO remove o pedido do carrinho — permite retry
    } else {
      // Erro de estoque (400) ou outro
      paymentModalError.value = error.message || 'Erro ao processar pedido.';
      await loadOrder(); // recarregar estado atualizado
    }
    paymentModalRef.value?.setState('error');
  } finally {
    isConfirming.value = false;
    pendingCardData.value = null;
  }
}

function onPaymentModalSuccess() {
  // Apenas aguarda o fechamento (manual ou automático)
}

function onPaymentModalClose() {
  const finalState = paymentModalRef.value?.state;
  isPaymentModalOpen.value = false;

  if (finalState === 'success' || finalState === 'error') {
    pendingCardData.value = null;
    router.push({ path: '/dashboard', query: { tab: 'historico-compra' } });
  } else if (selectedPaymentId.value === 3) {
    // Se o usuário apenas cancelou (idle) e o método era cartão, "volta" pro modal do cartão
    isCreditCardModalOpen.value = true;
  } else {
    pendingCardData.value = null;
  }
}

async function handleConfirmOrder() {
  if (!orderId.value || isReadOnly.value || isConfirming.value) return;

  // Cartão de crédito: coletar dados primeiro, depois abrir modal de pagamento
  if (selectedPaymentId.value === 3) {
    isCreditCardModalOpen.value = true;
    return;
  }

  // PIX / Boleto: abrir modal de confirmação direto
  pendingCardData.value = null;
  isPaymentModalOpen.value = true;
}

async function onCreditCardConfirm(cardData) {
  isCreditCardModalOpen.value = false;
  pendingCardData.value = cardData;
  isPaymentModalOpen.value = true;
}

async function executeCancelOrder() {
  if (!orderId.value) return;
  isCancelDialogOpen.value = false;
  isLoading.value = true;

  try {
    await deleteOrderApi(orderId.value);
    const producerId = checkoutProducer.value.id;
    if (producerId) {
      cartStore.removePendingOrderByProducer(producerId);
    }
    toast.info('Pedido descartado e removido do carrinho.', 'Compra descartada');
    router.push('/dashboard');
  } catch (error) {
    toast.error(error?.message || 'Não foi possível descartar o pedido.', 'Erro ao descartar');
    isLoading.value = false;
  }
}

onMounted(async () => {
  await loadOrder();
});

watch(orderId, async () => {
  await loadOrder();
});
</script>

<style scoped></style>
