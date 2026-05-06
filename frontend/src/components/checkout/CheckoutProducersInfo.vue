<template>
  <div class="rounded-2xl border border-slate-300 bg-white p-8">
    <h2 class="mb-6 text-xl font-extrabold text-slate-900">Informações do Produtor</h2>
    <div v-if="producer" class="space-y-4">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <p class="text-lg font-bold text-slate-900">{{ producer.name }}</p>
          <p class="mt-2 text-sm text-slate-600">📍 {{ producer.location }}</p>
          <p class="mt-1 text-sm text-slate-500">Distância: {{ producer.distance }} km</p>
        </div>
        <div
          v-if="producer.trusted"
          class="flex shrink-0 items-center gap-2 rounded-full bg-green-100 px-4 py-2 text-xs font-semibold text-green-700"
        >
          <span class="h-2 w-2 rounded-full bg-green-600"></span>
          Confiável
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * @typedef {import('@/types/checkout').Producer} Producer
 */

/**
 * Producer to display
 * @type {Producer}
 */
defineProps({
  producer: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped></style>
