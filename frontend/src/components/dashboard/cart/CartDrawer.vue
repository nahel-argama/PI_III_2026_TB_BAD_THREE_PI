<template>
  <Teleport to="body">
    <div v-if="modelValue" class="fixed inset-0 z-50">
      <div class="absolute inset-0 bg-slate-950/50" @click="closeDrawer"></div>

      <aside
        class="absolute top-0 right-0 flex h-full w-full max-w-xl flex-col border-l border-white/70 bg-white/95 shadow-2xl backdrop-blur-xl"
      >
        <header class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.24em] text-emerald-600">Carrinho</p>
            <h2 class="mt-1 text-xl font-black tracking-tight text-slate-900">Pedidos pendentes</h2>
          </div>
          <button
            type="button"
            class="rounded-xl border border-slate-200 bg-white p-2 text-slate-600 transition hover:border-slate-300 hover:text-slate-900"
            @click="closeDrawer"
          >
            <XMarkIcon class="h-5 w-5" />
          </button>
        </header>

        <div class="flex-1 overflow-y-auto p-5">
          <div v-if="!orders.length" class="rounded-2xl border border-dashed border-slate-200 bg-slate-50 px-6 py-10 text-center">
            <p class="text-sm font-semibold text-slate-700">Carrinho vazio</p>
            <p class="mt-2 text-xs text-slate-500">Adicione produtos em “Explorar Ofertas”.</p>
          </div>

          <div v-else class="space-y-4">
            <section
              v-for="order in orders"
              :key="order.id"
              class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
            >
              <div class="flex items-start justify-between gap-3">
                <div>
                  <p class="text-xs font-bold uppercase tracking-[0.22em] text-emerald-600">
                    Produtor
                  </p>
                  <h3 class="mt-1 text-base font-black text-slate-900">
                    {{ getProducerLabel(order) }}
                  </h3>
                  <p class="mt-1 text-xs text-slate-500">Pedido #{{ order.id }}</p>
                </div>
                <span class="rounded-full bg-amber-100 px-3 py-1 text-xs font-bold text-amber-800">
                  {{ order.status }}
                </span>
              </div>

              <div class="mt-4 space-y-3">
                <article
                  v-for="item in getOrderItems(order)"
                  :key="item.id"
                  class="rounded-xl border border-slate-100 bg-slate-50 p-3"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                      <p class="truncate text-sm font-bold text-slate-900">
                        {{ getItemName(item) }}
                      </p>
                      <p class="mt-1 text-xs text-slate-500">
                        Preço unitário: R$ {{ formatMoney(toNumber(item.unit_price)) }}
                      </p>
                    </div>
                    <button
                      type="button"
                      class="rounded-lg border border-rose-200 bg-white px-2 py-1 text-xs font-bold text-rose-600 transition hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-50"
                      :disabled="isItemLoading(order.id, item.id)"
                      @click="handleRemoveItem(order.id, item.id)"
                    >
                      Remover
                    </button>
                  </div>

                  <div class="mt-3 flex items-center justify-between gap-3">
                    <div class="flex items-center gap-2">
                      <button
                        type="button"
                        class="rounded-lg border border-slate-200 bg-white px-2 py-1 text-sm font-extrabold text-slate-700 transition hover:border-slate-300 disabled:cursor-not-allowed disabled:opacity-50"
                        :disabled="isItemLoading(order.id, item.id) || Number(item.quantity) <= 1"
                        @click="changeItemQuantity(order.id, item.id, Number(item.quantity) - 1)"
                      >
                        -
                      </button>
                      <span class="min-w-8 text-center text-sm font-bold text-slate-900">
                        {{ item.quantity }}
                      </span>
                      <button
                        type="button"
                        class="rounded-lg border border-slate-200 bg-white px-2 py-1 text-sm font-extrabold text-slate-700 transition hover:border-slate-300 disabled:cursor-not-allowed disabled:opacity-50"
                        :disabled="isItemLoading(order.id, item.id)"
                        @click="changeItemQuantity(order.id, item.id, Number(item.quantity) + 1)"
                      >
                        +
                      </button>
                    </div>

                    <p class="text-sm font-bold text-slate-900">
                      R$ {{ formatMoney(getLineTotal(item)) }}
                    </p>
                  </div>
                </article>
              </div>

              <div class="mt-4 space-y-2 border-t border-slate-100 pt-4">
                <div class="flex items-center justify-between text-sm text-slate-500">
                  <p>Subtotal (Produtos)</p>
                  <p>R$ {{ formatMoney(getOrderSubtotal(order)) }}</p>
                </div>
                
                <div class="flex items-center justify-between text-sm text-slate-500">
                  <p>Taxa da Plataforma (5%)</p>
                  <p>R$ {{ formatMoney(getOrderFee(order)) }}</p>
                </div>

                <div class="flex items-center justify-between pt-2 border-t border-slate-50">
                  <p class="text-sm font-semibold text-slate-600">Total do pedido</p>
                  <p class="text-lg font-black text-emerald-700">
                    R$ {{ formatMoney(getOrderTotal(order)) }}
                  </p>
                </div>

                <button
                  type="button"
                  class="mt-3 w-full rounded-xl bg-emerald-600 px-4 py-3 text-sm font-black text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300"
                  :disabled="getOrderItems(order).length === 0"
                  @click="$emit('checkout-order', order.id)"
                >
                  Finalizar pedido com {{ getProducerLabel(order) }}
                </button>
              </div>
            </section>
          </div>
        </div>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, ref } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';
import { useCartStore } from '@/stores/cart';
import { useToast } from '@/composables/useToast';

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:modelValue', 'checkout-order']);

const cartStore = useCartStore();
const toast = useToast();
const loadingMap = ref({});

const orders = computed(() => cartStore.pendingOrdersList);

function closeDrawer() {
  emit('update:modelValue', false);
}

function toNumber(value) {
  const nextValue = Number(value);
  return Number.isFinite(nextValue) ? nextValue : 0;
}

function formatMoney(value) {
  return toNumber(value).toFixed(2).replace('.', ',');
}

function getProducerLabel(order) {
  return `Produtor #${order?.producer ?? '-'}`;
}

function getOrderItems(order) {
  return Array.isArray(order?.items) ? order.items : [];
}

function getItemName(item) {
  return `Produto #${item?.product ?? '-'}`;
}

function getLineTotal(item) {
  return toNumber(item?.quantity) * toNumber(item?.unit_price);
}

function getOrderSubtotal(order) {
  const apiSubtotal = toNumber(order?.subtotal_value);
  if (apiSubtotal > 0) {
    return apiSubtotal;
  }
  return getOrderItems(order).reduce((sum, item) => sum + getLineTotal(item), 0);
}

function getOrderFee(order) {
  const apiFee = toNumber(order?.fee_value);
  if (apiFee > 0) {
    return apiFee;
  }
  return getOrderSubtotal(order) * 0.05;
}

function getOrderTotal(order) {
  const apiTotal = toNumber(order?.total_value);
  if (apiTotal > 0) {
    return apiTotal;
  }
  return getOrderSubtotal(order) + getOrderFee(order);
}

function getLoadingKey(orderId, itemId) {
  return `${orderId}:${itemId}`;
}

function isItemLoading(orderId, itemId) {
  return Boolean(loadingMap.value[getLoadingKey(orderId, itemId)]);
}

function setItemLoading(orderId, itemId, value) {
  const key = getLoadingKey(orderId, itemId);
  if (value) {
    loadingMap.value[key] = true;
    return;
  }

  delete loadingMap.value[key];
}

async function changeItemQuantity(orderId, itemId, nextQuantity) {
  const quantity = Number(nextQuantity);
  if (!quantity || quantity <= 0) {
    return;
  }

  setItemLoading(orderId, itemId, true);
  try {
    await cartStore.updateItem(orderId, itemId, quantity);
  } catch (error) {
    toast.error(error?.message || 'Não foi possível atualizar quantidade.', 'Erro no carrinho');
  } finally {
    setItemLoading(orderId, itemId, false);
  }
}

async function handleRemoveItem(orderId, itemId) {
  setItemLoading(orderId, itemId, true);
  try {
    await cartStore.removeItem(orderId, itemId);
  } catch (error) {
    toast.error(error?.message || 'Não foi possível remover item.', 'Erro no carrinho');
  } finally {
    setItemLoading(orderId, itemId, false);
  }
}
</script>
