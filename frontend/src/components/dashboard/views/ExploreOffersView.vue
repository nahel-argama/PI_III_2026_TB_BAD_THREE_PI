<template>
  <section class="space-y-6 pb-6">
    <OffersHeader
      :search="searchTerm"
      :item-count="filteredOffers.length"
      @update-search="searchTerm = $event"
    />

    <OffersGrid
      :items="filteredOffers"
      empty-title="Nenhuma oferta encontrada"
      empty-description="Tente outro termo de busca."
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import OffersGrid from './offers/OffersGrid.vue';
import OffersHeader from './offers/OffersHeader.vue';

const searchTerm = ref('');

const offers = ref([]);

const filteredOffers = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  return offers.value.filter((offer) => {
    const matchesSearch = [
      offer.productName,
      offer.supplierName,
      offer.supplierLocation,
      offer.category,
      offer.delivery,
    ]
      .join(' ')
      .toLowerCase()
      .includes(query);

    return matchesSearch;
  });
});
</script>
