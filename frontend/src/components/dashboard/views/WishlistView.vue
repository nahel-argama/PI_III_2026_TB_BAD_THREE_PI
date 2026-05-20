<template>
  <section class="space-y-6 pb-6">
    <WishlistToolbar
      :search="searchTerm"
      :loading="isLoading"
      @update-search="onSearch"
      @open-modal="isCreateModalOpen = true"
    />

    <WishlistGrid
      :items="wishlistItems"
      :loading="isLoading"
      @remove="removeProduct"
    />

    <AppPagination
      v-model="currentPage"
      :total-items="totalItems"
      @change="(page) => fetchItems(searchTerm, page)"
    />

    <WishlistCreateModal
      v-model="isCreateModalOpen"
      @submit="onItemCreated"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import WishlistCreateModal from './wishlist/WishlistCreateModal.vue';
import WishlistGrid from './wishlist/WishlistGrid.vue';
import WishlistToolbar from './wishlist/WishlistToolbar.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import { listWishlistItems } from '@/services/wishlist';

// ── State ─────────────────────────────────────────────────────────────────────

const searchTerm = ref('');
const isCreateModalOpen = ref(false);
const wishlistItems = ref([]);
const isLoading = ref(false);

const currentPage = ref(1);
const totalItems = ref(0);

// ── Fetch ─────────────────────────────────────────────────────────────────────

async function fetchItems(productName = '', page = 1) {
  isLoading.value = true;
  currentPage.value = page;
  try {
    const data = await listWishlistItems({ productName, page });
    wishlistItems.value = data.results;
    totalItems.value = data.count || 0;
  } catch {
    wishlistItems.value = [];
    totalItems.value = 0;
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => fetchItems());

// ── Search (debounced, delegado à API) ────────────────────────────────────────

let searchTimer = null;

function onSearch(value) {
  searchTerm.value = value;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => fetchItems(value.trim()), 400);
}

// ── Actions ───────────────────────────────────────────────────────────────────

/** Chamado após o modal criar o item com sucesso — insere no topo da lista. */
function onItemCreated(newItem) {
  wishlistItems.value.unshift(newItem);
  totalItems.value++;
}

async function removeProduct(itemId) {
  // Remove otimisticamente do estado local
  wishlistItems.value = wishlistItems.value.filter((item) => item.id !== itemId);

  // Se a página atual ficou vazia e não for a primeira página, voltamos para a página anterior
  let targetPage = currentPage.value;
  if (wishlistItems.value.length === 0 && currentPage.value > 1) {
    targetPage = currentPage.value - 1;
  }

  // Recarrega os dados do backend para sincronizar a listagem e os totais de paginação
  await fetchItems(searchTerm.value, targetPage);
}
</script>
