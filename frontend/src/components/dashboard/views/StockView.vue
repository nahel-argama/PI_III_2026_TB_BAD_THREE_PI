<template>
  <section class="space-y-6 pb-6">
    <StockToolbar
      :search="searchTerm"
      :loading="isLoading"
      @update-search="onSearch"
      @open-modal="isCreateModalOpen = true"
    />

    <StockGrid
      :items="products"
      :loading="isLoading"
      @remove="removeProductHandler"
    />

    <AppPagination
      v-model="currentPage"
      :total-items="totalItems"
      @change="(page) => fetchItems(searchTerm, page)"
    />

    <StockCreateModal
      v-model="isCreateModalOpen"
      @submit="onProductCreated"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StockCreateModal from './stock/StockCreateModal.vue';
import StockGrid from './stock/StockGrid.vue';
import StockToolbar from './stock/StockToolbar.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import { listProducts } from '@/services/product';
import { useToast } from '@/composables/useToast';
import { capitalize } from '@/utils/string';

const toast = useToast();

const searchTerm = ref('');
const isCreateModalOpen = ref(false);
const products = ref([]);
const isLoading = ref(false);

const currentPage = ref(1);
const totalItems = ref(0);

async function fetchItems(query = '', page = 1) {
  isLoading.value = true;
  currentPage.value = page;
  try {
    const data = await listProducts({ query, page });
    products.value = data.results || data;
    totalItems.value = data.count || products.value.length;
  } catch {
    products.value = [];
    totalItems.value = 0;
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => fetchItems());

let searchTimer = null;

function onSearch(value) {
  searchTerm.value = value;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => fetchItems(value.trim()), 400);
}

function onProductCreated(newProduct) {
  products.value.push(newProduct);
  totalItems.value++;

  const name = newProduct.name ? capitalize(newProduct.name) : 'Produto';
  toast.success(`"${name}" foi adicionado ao estoque com sucesso!`, 'Adicionado');
}

async function removeProductHandler(itemId) {
  products.value = products.value.filter((item) => item.id !== itemId);

  let targetPage = currentPage.value;
  if (products.value.length === 0 && currentPage.value > 1) {
    targetPage = currentPage.value - 1;
  }

  await fetchItems(searchTerm.value, targetPage);
}
</script>
