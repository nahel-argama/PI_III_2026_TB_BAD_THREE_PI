<template>
  <header class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.28em] text-emerald-600">
          {{ eyebrow }}
        </p>
        <h2 class="mt-2 text-3xl font-black tracking-tight text-slate-900">
          {{ title }}
        </h2>
        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
          {{ description }}
        </p>
      </div>

      <div class="flex w-full flex-col gap-3 sm:flex-row sm:items-center lg:w-auto">
        <label class="relative block w-full sm:w-80" for="history-search">
          <span class="sr-only">Buscar histórico</span>
          <input
            id="history-search"
            :value="search"
            type="text"
            class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 pr-11 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-300 focus:ring-4 focus:ring-emerald-100"
            placeholder="Buscar no histórico..."
            @input="$emit('update-search', $event.target.value)"
          />
          <MagnifyingGlassIcon class="pointer-events-none absolute right-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
        </label>

        <div class="inline-flex items-center gap-2 rounded-2xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-700">
          <ClockIcon class="h-5 w-5" />
          {{ itemCount }} {{ actionLabel }}
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ClockIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline';

defineProps({
  eyebrow: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  search: {
    type: String,
    default: '',
  },
  itemCount: {
    type: Number,
    default: 0,
  },
  actionLabel: {
    type: String,
    required: true,
  },
});

defineEmits(['update-search']);
</script>
