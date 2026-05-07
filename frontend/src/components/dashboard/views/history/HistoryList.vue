<template>
  <section>
    <div
      v-if="items.length"
      class="space-y-3"
    >
      <HistoryAccordionItem
        v-for="item in items"
        :key="item.id"
        :item="item"
        :item-kind-label="itemKindLabel"
        :is-open="openItemId === item.id"
        @toggle="toggleItem"
      />
    </div>

    <div
      v-else
      class="rounded-[28px] border border-dashed border-slate-200 bg-white/70 px-6 py-16 text-center"
    >
      <p class="text-xs font-bold uppercase tracking-[0.28em] text-emerald-600">
        Sem resultados
      </p>
      <h3 class="mt-3 text-2xl font-black tracking-tight text-slate-900">
        {{ emptyTitle }}
      </h3>
      <p class="mx-auto mt-3 max-w-md text-sm leading-6 text-slate-600">
        {{ emptyDescription }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import HistoryAccordionItem from './HistoryAccordionItem.vue';

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  emptyTitle: {
    type: String,
    required: true,
  },
  emptyDescription: {
    type: String,
    required: true,
  },
  itemKindLabel: {
    type: String,
    required: true,
  },
});

const openItemId = ref(null);

function toggleItem(itemId) {
  openItemId.value = openItemId.value === itemId ? null : itemId;
}

</script>
