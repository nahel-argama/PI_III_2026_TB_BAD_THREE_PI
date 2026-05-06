<template>
  <div class="rounded-2xl border border-slate-300 bg-white p-8">
    <h2 class="mb-6 text-xl font-extrabold text-slate-900">Resumo de Valores</h2>

    <div class="space-y-4">
      <div class="flex justify-between">
        <span class="text-slate-600">Subtotal em Produtos</span>
        <span class="font-semibold text-slate-900">R$ {{ subtotal.toFixed(2) }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-600">Taxa da Plataforma</span>
        <span class="font-semibold text-slate-900">R$ {{ platformFee.toFixed(2) }}</span>
      </div>
      <div class="border-t border-slate-200 pt-4">
        <div class="flex justify-between">
          <span class="font-bold text-slate-900">Total</span>
          <span class="text-2xl font-extrabold text-green-600">R$ {{ total.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Pricing props for display
 */
defineProps({
  subtotal: {
    type: Number,
    required: true,
  },
  platformFee: {
    type: Number,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
});
</script>

<style scoped></style>
