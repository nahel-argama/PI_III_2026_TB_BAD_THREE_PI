<template>
  <header
    class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6"
  >
    <div class="flex flex-col gap-5">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 class="mt-2 text-3xl font-black tracking-tight text-slate-900">Explorar Ofertas</h2>
        </div>

        <label class="relative block w-full sm:w-96" for="offers-search">
          <span class="sr-only">Buscar oferta</span>
          <input
            id="offers-search"
            :value="search"
            type="text"
            class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 pr-11 text-sm text-slate-900 transition outline-none placeholder:text-slate-400 focus:border-emerald-300 focus:ring-4 focus:ring-emerald-100"
            placeholder="Buscar produto, fornecedor ou região..."
            @input="$emit('update-search', $event.target.value)"
          />
          <MagnifyingGlassIcon
            class="pointer-events-none absolute top-1/2 right-4 h-5 w-5 -translate-y-1/2 text-slate-400"
          />
        </label>
      </div>
    </div>
  </header>
</template>

<script setup>
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline';

defineProps({
  search: {
    type: String,
    default: '',
  },
  itemCount: {
    type: Number,
    default: 0,
  },
});

defineEmits(['update-search']);
</script>
