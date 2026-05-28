<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
    <div class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur">
      <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Produtos Ranqueados</p>
      <p class="mt-2 text-2xl font-bold text-slate-800">
        <span v-if="isLoading" class="inline-block animate-pulse bg-slate-200 text-transparent rounded w-12">--</span>
        <span v-else>{{ data?.results?.length || 0 }}</span>
      </p>
    </div>
    <div class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur">
      <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total de Desejos</p>
      <p class="mt-2 text-2xl font-bold text-slate-800">
        <span v-if="isLoading" class="inline-block animate-pulse bg-slate-200 text-transparent rounded w-16">--</span>
        <span v-else>{{ data?.total_items || 0 }}</span>
      </p>
    </div>
    <div class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur">
      <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Produto Mais Desejado</p>
      <p class="mt-2 text-xl font-bold text-emerald-600 truncate">
        <span v-if="isLoading" class="inline-block animate-pulse bg-slate-200 text-transparent rounded w-32">Carregando...</span>
        <span v-else>{{ data?.results?.[0]?.product_name ? capitalize(data.results[0].product_name) : 'Nenhum' }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: { type: Object, default: () => null },
  isLoading: { type: Boolean, default: false }
});
</script>
