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

const offers = ref([
  {
    id: 1,
    productName: 'Tomate Italiano',
    supplierName: 'Sítio Boa Vista',
    supplierLocation: 'Valinhos - SP',
    category: 'Hortaliças',
    unit: 'caixa',
    stock: '180 kg',
    delivery: 'Entrega em 24h',
    statusTone: 'emerald',
  },
  {
    id: 2,
    productName: 'Maçã Gala',
    supplierName: 'Cooperativa Serra Fresca',
    supplierLocation: 'Limeira - SP',
    category: 'Frutas',
    unit: 'fardo',
    stock: '240 kg',
    delivery: 'Entrega em 48h',
    statusTone: 'blue',
  },
  {
    id: 3,
    productName: 'Alface Crespa',
    supplierName: 'Horta Bela Aurora',
    supplierLocation: 'Sorocaba - SP',
    category: 'Folhosas',
    unit: 'molho',
    stock: '95 molhos',
    delivery: 'Entrega hoje',
    statusTone: 'amber',
  },
  {
    id: 4,
    productName: 'Banana Prata',
    supplierName: 'Rancho Vale Verde',
    supplierLocation: 'Mogi Mirim - SP',
    category: 'Frutas',
    unit: 'caixa',
    stock: '210 kg',
    delivery: 'Entrega em 72h',
    statusTone: 'emerald',
  },
  {
    id: 5,
    productName: 'Cenoura Extra',
    supplierName: 'Fazenda Horizonte',
    supplierLocation: 'Itatiba - SP',
    category: 'Hortaliças',
    unit: 'saco',
    stock: '130 kg',
    delivery: 'Entrega em 24h',
    statusTone: 'blue',
  },
]);

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
