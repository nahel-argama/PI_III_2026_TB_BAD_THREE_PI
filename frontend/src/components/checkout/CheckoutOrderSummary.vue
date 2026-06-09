<template>
  <div class="rounded-2xl border border-slate-300 bg-white p-8">
    <h2 class="mb-6 text-xl font-extrabold text-slate-900">Resumo do Pedido</h2>

    <div
      v-if="!items.length"
      class="rounded-xl border border-dashed border-slate-200 bg-slate-50 px-4 py-6 text-sm text-slate-600"
    >
      Este pedido não possui itens.
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="item in items"
        :key="item.id"
        class="flex gap-4 border-b border-slate-200 pb-6 last:border-0"
      >
        <div
          v-if="item.imageUrl"
          class="h-20 w-20 flex-shrink-0 overflow-hidden rounded-lg border border-slate-200"
        >
          <AppSecureImage
            :src="item.imageUrl"
            :alt="item.name"
            object-fit-class="object-cover"
          />
        </div>
        <div
          v-else
          class="flex h-20 w-20 flex-shrink-0 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-xs font-bold text-slate-500"
        >
          #{{ item.productId }}
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-slate-900">{{ item.name }}</h3>

          <div class="mt-3 space-y-1 text-xs text-slate-600">
            <div>
              Quantidade: <span class="font-semibold text-slate-900">{{ item.quantity }} kg</span>
            </div>
            <div>
              Preço unitário:
              <span class="font-semibold text-slate-900">R$ {{ item.pricePerKg.toFixed(2) }} / kg</span>
            </div>
          </div>
        </div>
        <div class="text-right">
          <p class="text-sm text-slate-600">Total</p>
          <p class="text-lg font-bold text-slate-900">
            R$ {{ calculateItemTotal(item).toFixed(2) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppSecureImage from '@/components/ui/AppSecureImage.vue';

/**
 * @typedef {import('@/types/checkout').OrderItem} OrderItem
 */

/**
 * Order items to display
 * @type {OrderItem[]}
 */
defineProps({
  items: {
    type: Array,
    required: true,
  },
});

/**
 * Calculate total for a single item
 * @param {OrderItem} item
 * @returns {number}
 */
const calculateItemTotal = (item) => item.quantity * item.pricePerKg;
</script>

<style scoped></style>
