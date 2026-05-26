<template>
  <section>
    <div
      v-if="items.length"
      class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3"
    >
      <OfferCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        :cart-quantity="Number(cartQuantities[item.id] || 0)"
        :is-adding="Number(addingProductId) === Number(item.id)"
        @add-to-cart="$emit('add-to-cart', $event)"
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
import OfferCard from './OfferCard.vue';

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
  cartQuantities: {
    type: Object,
    default: () => ({}),
  },
  addingProductId: {
    type: [Number, String],
    default: null,
  },
});

defineEmits(['add-to-cart']);
</script>
