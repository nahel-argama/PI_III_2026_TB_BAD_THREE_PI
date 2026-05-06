<template>
  <div class="rounded-2xl border border-slate-300 bg-white p-8">
    <h2 class="mb-6 text-xl font-extrabold text-slate-900">Resumo do Pedido</h2>

    <div class="space-y-6">
      <div
        v-for="item in items"
        :key="item.id"
        class="flex gap-4 border-b border-slate-200 pb-6 last:border-0"
      >
        <img
          :src="item.image"
          :alt="item.name"
          class="h-20 w-20 flex-shrink-0 rounded-lg object-cover"
        />
        <div class="flex-1">
          <h3 class="font-bold text-slate-900">{{ item.name }}</h3>
          <p class="text-sm text-slate-600">Produtor: {{ item.producer }}</p>

          <div class="mt-3 space-y-1 text-xs text-slate-600">
            <div>
              Quantidade: <span class="font-semibold text-slate-900">{{ item.quantity }} kg</span>
            </div>
            <div>
              Preço/kg:
              <span class="font-semibold text-slate-900">R$ {{ item.pricePerKg.toFixed(2) }}</span>
            </div>
            <div>
              Distância: <span class="font-semibold text-slate-900">{{ item.distance }} km</span>
            </div>
            <div v-if="item.inStock" class="flex items-center gap-2 text-green-700">
              <div class="h-2 w-2 rounded-full bg-green-600"></div>
              <span class="font-semibold">Disponibilidade: Pronta Entrega</span>
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
