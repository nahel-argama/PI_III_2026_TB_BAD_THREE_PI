<template>
  <div class="rounded-2xl border border-slate-300 bg-white p-8">
    <h2 class="mb-6 text-xl font-extrabold text-slate-900">Informações do Produtor</h2>
    <div v-if="producer" class="space-y-4">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <p class="text-lg font-bold text-slate-900">{{ producer.name || 'Produtor não identificado' }}</p>
          <p class="mt-2 text-sm text-slate-600">
            Identificador: #{{ producer.id ?? '-' }}
          </p>
        </div>
        <div
          class="flex shrink-0 items-center gap-2 rounded-full px-4 py-2 text-xs font-semibold"
          :class="statusTone"
        >
          <span class="h-2 w-2 rounded-full" :class="statusDotTone"></span>
          {{ orderStatus || 'SEM STATUS' }}
        </div>
      </div>
    </div>

    <div v-else class="rounded-xl border border-dashed border-slate-200 bg-slate-50 px-4 py-5 text-sm text-slate-600">
      Informações do produtor indisponíveis no momento.
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

/**
 * @typedef {import('@/types/checkout').Producer} Producer
 */

const props = defineProps({
  producer: {
    type: Object,
    default: null,
  },
  orderStatus: {
    type: String,
    default: '',
  },
});

const statusTone = computed(() => {
  if (props.orderStatus === 'PENDING') return 'bg-amber-100 text-amber-800';
  if (props.orderStatus === 'CONFIRMED') return 'bg-emerald-100 text-emerald-800';
  if (props.orderStatus === 'CANCELED') return 'bg-rose-100 text-rose-800';
  if (props.orderStatus === 'DELIVERED') return 'bg-blue-100 text-blue-800';
  return 'bg-slate-100 text-slate-700';
});

const statusDotTone = computed(() => {
  if (props.orderStatus === 'PENDING') return 'bg-amber-600';
  if (props.orderStatus === 'CONFIRMED') return 'bg-emerald-600';
  if (props.orderStatus === 'CANCELED') return 'bg-rose-600';
  if (props.orderStatus === 'DELIVERED') return 'bg-blue-600';
  return 'bg-slate-500';
});
</script>

<style scoped></style>
