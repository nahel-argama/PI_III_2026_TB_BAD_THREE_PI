<template>
  <section class="space-y-6 pb-6">
    <ProductImagesHeader
      :search="searchTerm"
      :item-count="filteredProducts.length"
      @update-search="searchTerm = $event"
      @open-modal="openCreateModal"
    />

    <ProductImagesGrid :items="filteredProducts" @edit="openEditModal" @remove="removeProduct" />

    <ProductImageFormModal
      v-model="isModalOpen"
      :mode="modalMode"
      :initial-value="selectedProduct"
      @submit="handleSubmit"
    />
  </section>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import {
  listDefaultProductImages,
  uploadDefaultProductImage,
} from '@/services/defaultProductImages';
import ProductImageFormModal from './product-images/ProductImageFormModal.vue';
import ProductImagesGrid from './product-images/ProductImagesGrid.vue';
import ProductImagesHeader from './product-images/ProductImagesHeader.vue';

const searchTerm = ref('');
const isModalOpen = ref(false);
const modalMode = ref('create');
const selectedProductId = ref(null);
const currentPage = ref(1);

const products = ref([]);

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

async function fetchProducts() {
  try {
    const data = await listDefaultProductImages({ page: currentPage.value });
    const results = data.results || data || [];
    products.value = results.map((item) => ({
      id: item.id,
      product_external_key: item.product_external_key,
      name: item.product?.name || item.product_name || 'Produto',
      imageUrl: item.image_url || item.image || item.imageUrl,
    }));
  } catch {
    // Silently catch listing error
  }
}

onMounted(() => {
  fetchProducts();
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

async function handleSubmit(payload) {
  if (!payload.productId || !payload.imageUrl) return;

  try {
    await uploadDefaultProductImage(payload.productId, payload.imageUrl);
    await fetchProducts();
  } catch {
    // Silently catch upload error
  }
}

function removeProduct() {
  // Nota: Não há rota de remoção conforme especificação ("somente essas duas rotas")
}
</script>
