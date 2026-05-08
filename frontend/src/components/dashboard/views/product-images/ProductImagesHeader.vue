<template>
  <header class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.28em] text-emerald-600">
          Varejista
        </p>
        <h2 class="mt-2 text-3xl font-black tracking-tight text-slate-900">
          Gerenciar Imagens de Produtos
        </h2>
        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
          TODO: mover esta funcionalidade para ADMIN quando o backend suportar o novo tipo de usuário.
        </p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <label class="relative block w-full sm:w-80" for="product-images-search">
          <span class="sr-only">Buscar produto</span>
          <input
            id="product-images-search"
            :value="search"
            type="text"
            class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 pr-11 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-300 focus:ring-4 focus:ring-emerald-100"
            placeholder="Buscar produto..."
            @input="$emit('update-search', $event.target.value)"
          />
          <MagnifyingGlassIcon class="pointer-events-none absolute right-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
        </label>

        <button
          type="button"
          class="inline-flex items-center justify-center gap-2 rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-600/25 transition hover:bg-emerald-700"
          @click="$emit('open-modal')"
        >
          <PlusIcon class="h-5 w-5" />
          Adicionar produto
        </button>
      </div>
    </div>

    <p class="mt-4 text-sm font-medium text-slate-500">
      {{ itemCount }} produto(s) na tela
    </p>
  </header>
</template>

<script setup>
import { MagnifyingGlassIcon, PlusIcon } from '@heroicons/vue/24/outline';

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

defineEmits(['open-modal', 'update-search']);
</script>
