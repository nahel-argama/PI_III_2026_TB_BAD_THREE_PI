<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
    <div
      class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur"
    >
      <p class="text-xs font-semibold tracking-wider text-slate-400 uppercase">
        Produtos Ranqueados
      </p>
      <p class="mt-2 text-2xl font-bold text-slate-800">
        <span
          v-if="isLoading"
          class="inline-block w-12 animate-pulse rounded bg-slate-200 text-transparent"
          >--</span
        >
        <span v-else>{{ data?.results?.length || 0 }}</span>
      </p>
    </div>
    <div
      class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur"
    >
      <p class="text-xs font-semibold tracking-wider text-slate-400 uppercase">Total de Desejos</p>
      <p class="mt-2 text-2xl font-bold text-slate-800">
        <span
          v-if="isLoading"
          class="inline-block w-16 animate-pulse rounded bg-slate-200 text-transparent"
          >--</span
        >
        <span v-else>{{ data?.total_items || 0 }}</span>
      </p>
    </div>
    <div
      class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur"
    >
      <p class="text-xs font-semibold tracking-wider text-slate-400 uppercase">
        Produto Mais Desejado
      </p>
      <p class="mt-2 truncate text-xl font-bold text-emerald-600">
        <span
          v-if="isLoading"
          class="inline-block w-32 animate-pulse rounded bg-slate-200 text-transparent"
          >Carregando...</span
        >
        <span v-else>{{
          data?.results?.[0]?.product_name ? capitalize(data.results[0].product_name) : 'Nenhum'
        }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: { type: Object, default: () => null },
  isLoading: { type: Boolean, default: false },
});
</script>
