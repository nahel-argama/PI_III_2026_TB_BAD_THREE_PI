<template>
  <section class="space-y-6 pb-6">
    <ProductImagesHeader
      :search="searchTerm"
      :item-count="filteredProducts.length"
      @update-search="searchTerm = $event"
      @open-modal="openCreateModal"
    />

    <ProductImagesGrid
      :items="filteredProducts"
      @edit="openEditModal"
      @remove="removeProduct"
    />

    <ProductImageFormModal
      v-model="isModalOpen"
      :mode="modalMode"
      :initial-value="selectedProduct"
      @submit="handleSubmit"
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import ProductImageFormModal from './product-images/ProductImageFormModal.vue';
import ProductImagesGrid from './product-images/ProductImagesGrid.vue';
import ProductImagesHeader from './product-images/ProductImagesHeader.vue';

const searchTerm = ref('');
const isModalOpen = ref(false);
const modalMode = ref('create');
const selectedProductId = ref(null);

const products = ref([
  {
    id: 1,
    name: 'Tomate Italiano',
    imageUrl:
      'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 2,
    name: 'Alface Crespa',
    imageUrl:
      'https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 3,
    name: 'Banana Prata',
    imageUrl:
      'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=900&q=80',
  },
]);

const filteredProducts = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return products.value;
  }

  return products.value.filter((product) => product.name.toLowerCase().includes(query));
});

const selectedProduct = computed(() => {
  return products.value.find((product) => product.id === selectedProductId.value) || null;
});

function openCreateModal() {
  selectedProductId.value = null;
  modalMode.value = 'create';
  isModalOpen.value = true;
}

function openEditModal(productId) {
  selectedProductId.value = productId;
  modalMode.value = 'edit';
  isModalOpen.value = true;
}

function handleSubmit(payload) {
  if (modalMode.value === 'edit' && selectedProductId.value) {
    products.value = products.value.map((product) => {
      if (product.id !== selectedProductId.value) {
        return product;
      }

      return {
        ...product,
        imageUrl: payload.imageUrl,
      };
    });
    return;
  }

  products.value.unshift({
    id: Date.now(),
    name: payload.name,
    imageUrl: payload.imageUrl,
  });
}

function removeProduct(productId) {
  products.value = products.value.filter((product) => product.id !== productId);
}
</script>
