<template>
  <section class="space-y-6 pb-6">
    <WishlistToolbar
      :search="searchTerm"
      :item-count="wishlistItems.length"
      :loading="isLoading"
      @update-search="onSearch"
      @open-modal="isCreateModalOpen = true"
    />

    <WishlistGrid
      :items="wishlistItems"
      :loading="isLoading"
      @remove="removeProduct"
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
import { listWishlistItems } from '@/services/wishlist';

// ── State ─────────────────────────────────────────────────────────────────────

const searchTerm = ref('');
const isCreateModalOpen = ref(false);
const wishlistItems = ref([]);
const isLoading = ref(false);

// ── Fetch ─────────────────────────────────────────────────────────────────────

async function fetchItems(productName = '') {
  isLoading.value = true;
  try {
    const data = await listWishlistItems({ productName });
    wishlistItems.value = data.results;
  } catch (err) {
    console.error('[WishlistView] Falha ao carregar itens:', err);
    wishlistItems.value = [];
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
}

function removeProduct(itemId) {
  wishlistItems.value = wishlistItems.value.filter((item) => item.id !== itemId);
}
</script>
