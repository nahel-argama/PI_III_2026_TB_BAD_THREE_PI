<template>
  <section class="space-y-6 pb-6">
    <OffersHeader
      :search="searchTerm"
      @update-search="onSearch"
    />

    <OffersGrid
      :items="offers"
      empty-title="Nenhuma oferta encontrada"
      empty-description="Tente outro termo de busca."
    />

    <AppPagination
      v-model="currentPage"
      :total-items="totalItems"
      @change="(page) => fetchOffers(searchTerm, page)"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import OffersGrid from './offers/OffersGrid.vue';
import OffersHeader from './offers/OffersHeader.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import { listProducts } from '@/services/product';

const searchTerm = ref('');
const offers = ref([]);
const isLoading = ref(false);

const currentPage = ref(1);
const totalItems = ref(0);

async function fetchOffers(query = '', page = 1) {
  isLoading.value = true;
  currentPage.value = page;
  try {
    const data = await listProducts({ query, page });
    offers.value = data.results;
    totalItems.value = data.count || 0;
  } catch {
    offers.value = [];
    totalItems.value = 0;
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => fetchOffers());

let searchTimer = null;

function onSearch(value) {
  searchTerm.value = value;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => fetchOffers(value.trim()), 400);
}
</script>
