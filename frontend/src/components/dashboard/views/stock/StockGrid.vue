<template>
  <section>
    <div v-if="items.length" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      <StockProductCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        @remove="$emit('remove', $event)"
      />
    </div>

    <div
      v-else
      class="rounded-[28px] border border-dashed border-slate-200 bg-white/70 px-6 py-16 text-center"
    >
      <p class="text-xs font-bold tracking-[0.28em] text-emerald-600 uppercase">Sem resultados</p>
      <h3 class="mt-3 text-2xl font-black tracking-tight text-slate-900">
        Nenhum produto em estoque
      </h3>
      <p class="mx-auto mt-3 max-w-md text-sm leading-6 text-slate-600">
        Você ainda não possui produtos no seu estoque ou a busca não retornou resultados. Adicione
        produtos pelo botão acima.
      </p>
    </div>
  </section>
</template>

<script setup>
import StockProductCard from './StockProductCard.vue';

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});

defineEmits(['remove']);
</script>
