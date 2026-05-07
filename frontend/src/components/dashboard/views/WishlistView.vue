<template>
  <section class="space-y-6 pb-6">
    <WishlistToolbar
      :search="searchTerm"
      :item-count="filteredProducts.length"
      @update-search="searchTerm = $event"
      @open-modal="isCreateModalOpen = true"
    />

    <WishlistGrid
      :items="filteredProducts"
      @remove="removeProduct"
    />

    <WishlistCreateModal
      v-model="isCreateModalOpen"
      @submit="addProduct"
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import WishlistCreateModal from './wishlist/WishlistCreateModal.vue';
import WishlistGrid from './wishlist/WishlistGrid.vue';
import WishlistToolbar from './wishlist/WishlistToolbar.vue';

const searchTerm = ref('');
const isCreateModalOpen = ref(false);

const wishlistProducts = ref([
  {
    id: 1,
    name: 'Tomate Italiano',
  },
  {
    id: 2,
    name: 'Maçã Gala',
  },
  {
    id: 3,
    name: 'Alface Crespa',
  },
  {
    id: 4,
    name: 'Banana Prata',
  },
]);

const filteredProducts = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return wishlistProducts.value;
  }

  return wishlistProducts.value.filter((product) => {
    return product.name.toLowerCase().includes(query);
  });
});

function addProduct(newProduct) {
  wishlistProducts.value.unshift({
    ...newProduct,
    id: Date.now(),
  });
}

function removeProduct(productId) {
  wishlistProducts.value = wishlistProducts.value.filter((product) => product.id !== productId);
}
</script>
