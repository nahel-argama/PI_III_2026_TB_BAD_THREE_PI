<template>
  <div class="rounded-2xl border border-slate-300 bg-white p-8">
    <h2 class="mb-6 text-xl font-extrabold text-slate-900">Método de Pagamento</h2>

    <div class="space-y-3">
      <label
        v-for="method in availableMethods"
        :key="method.id"
        class="flex cursor-pointer items-start gap-4 rounded-xl border-2 border-slate-300 p-4 transition hover:border-green-500"
        :class="{ 'border-green-600 bg-green-50': selectedPaymentId === method.id }"
      >
        <input
          type="radio"
          :value="method.id"
          :checked="selectedPaymentId === method.id"
          @change="onSelectPaymentMethod(method.id)"
          class="mt-1 h-5 w-5 accent-green-600"
        />
        <div>
          <p class="font-bold text-slate-900">{{ method.name }}</p>
          <p class="text-xs text-slate-600">{{ method.description }}</p>
        </div>
      </label>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

/**
 * All available payment method options defined in the component
 */
const allPaymentMethods = [
  {
    id: 1,
    name: 'Pix',
    description: 'Transferência instantânea',
  },
  {
    id: 2,
    name: 'Boleto Bancário',
    description: 'Faturado em 15 dias',
  },
  {
    id: 3,
    name: 'Cartão de Crédito B2B',
    description: 'Parcelado em até 12x',
  },
];

const props = defineProps({
  /**
   * Currently selected payment method ID
   * @type {number}
   */
  selectedPaymentId: {
    type: Number,
    required: true,
  },
  /**
   * Enable Pix payment method
   * @type {boolean}
   */
  pix: {
    type: Boolean,
    default: true,
  },
  /**
   * Enable Boleto payment method
   * @type {boolean}
   */
  boleto: {
    type: Boolean,
    default: true,
  },
  /**
   * Enable Credit Card payment method
   * @type {boolean}
   */
  creditCard: {
    type: Boolean,
    default: true,
  },
  /**
   * Callback function when payment method is selected
   * @type {Function}
   */
  onSelectPaymentMethod: {
    type: Function,
    required: true,
  },
});

/**
 * Filter payment methods based on enabled flags
 */
const availableMethods = computed(() => {
  return allPaymentMethods.filter((method) => {
    if (method.id === 1) return props.pix;
    if (method.id === 2) return props.boleto;
    if (method.id === 3) return props.creditCard;
    return false;
  });
});
</script>

<style scoped></style>
