<template>
  <div class="checkout-container min-h-screen bg-white">
    <CheckoutHeader />

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

        <div v-else-if="isLoading" class="rounded-2xl border border-slate-200 bg-white p-8 text-center">
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
            <CheckoutProducersInfo :producer="checkoutProducer" :order-status="order?.status || null" />
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
      v-model="isErrorDialogOpen"
      variant="warning"
      title="Não foi possível confirmar o pedido"
      :message="confirmErrorMessage"
      confirm-label="Ok, revisar pedido"
      :show-cancel="false"
      @confirm="isErrorDialogOpen = false"
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
import { getOrder } from '@/services/ordersService';
import { getProductById } from '@/services/product';
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
const isErrorDialogOpen = ref(false);
const confirmErrorMessage = ref('');
const productDetailsMap = ref({});

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
    const productId = Number(item?.product);
    const productDetails = productDetailsMap.value[productId] || null;
    const unitPrice = Number(item?.unit_price || 0);

    return {
      id: item.id,
      name: productDetails?.name || `Produto #${item.product}`,
      productId: item.product,
      quantity: Number(item.quantity || 0),
      pricePerKg: unitPrice,
      lineTotal: Number(item.quantity || 0) * unitPrice,
      imageUrl: productDetails?.images?.[0]?.image || null,
    };
  });
});

const checkoutProducer = computed(() => {
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
  return checkoutItems.value.reduce((sum, item) => sum + Number(item.lineTotal || 0), 0);
});

const platformFee = computed(() => 0);

const total = computed(() => {
  const apiTotal = Number(order.value?.total_value || 0);
  if (apiTotal > 0) {
    return apiTotal;
  }
  return subtotal.value + platformFee.value;
});

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
  productDetailsMap.value = {};

  try {
    const fetchedOrder = await getOrder(orderId.value);
    order.value = fetchedOrder;
    cartStore.setPendingOrder(fetchedOrder);
    await loadProductDetails(fetchedOrder);
  } catch (error) {
    pageError.value = error?.message || 'Não foi possível carregar o pedido.';
  } finally {
    isLoading.value = false;
  }
}

async function loadProductDetails(orderData) {
  const items = Array.isArray(orderData?.items) ? orderData.items : [];
  const uniqueProductIds = [...new Set(items.map((item) => Number(item?.product)).filter(Boolean))];

  if (!uniqueProductIds.length) {
    productDetailsMap.value = {};
    return;
  }

  const results = await Promise.allSettled(uniqueProductIds.map((productId) => getProductById(productId)));
  const nextMap = {};

  results.forEach((result, index) => {
    if (result.status !== 'fulfilled') {
      return;
    }

    const productId = uniqueProductIds[index];
    nextMap[productId] = result.value;
  });

  productDetailsMap.value = nextMap;
}

async function handleConfirmOrder() {
  if (!orderId.value || isReadOnly.value || isConfirming.value) {
    return;
  }

  isConfirming.value = true;

  try {
    const confirmedOrder = await cartStore.confirmOrder(orderId.value);
    order.value = confirmedOrder;

    toast.success('Pedido confirmado com sucesso.', 'Compra finalizada');
    await router.push({
      path: '/dashboard',
      query: { tab: 'historico-compra' },
    });
  } catch (error) {
    confirmErrorMessage.value =
      error?.message ||
      'O estoque foi alterado. Revise as quantidades antes de tentar novamente.';
    isErrorDialogOpen.value = true;

    await loadOrder();
  } finally {
    isConfirming.value = false;
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
