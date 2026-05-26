<template>
  <section class="space-y-6 pb-6">
    <OffersHeader
      :search="searchTerm"
      @update-search="onSearch"
    />

    <OffersGrid
      :items="offers"
      :cart-quantities="cartQuantitiesByProduct"
      :adding-product-id="addingProductId"
      empty-title="Nenhuma oferta encontrada"
      empty-description="Tente outro termo de busca."
      @add-to-cart="handleAddToCart"
    />

    <AppPagination
      v-model="currentPage"
      :total-items="totalItems"
      @change="(page) => fetchOffers(searchTerm, page)"
    />
  </section>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import OffersGrid from './offers/OffersGrid.vue';
import OffersHeader from './offers/OffersHeader.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import { listProducts } from '@/services/product';
import { useCartStore } from '@/stores/cart';
import { useToast } from '@/composables/useToast';
import { capitalize } from '@/utils/string';

const searchTerm = ref('');
const offers = ref([]);
const isLoading = ref(false);
const addingProductId = ref(null);

const currentPage = ref(1);
const totalItems = ref(0);
const cartStore = useCartStore();
const toast = useToast();

const cartQuantitiesByProduct = computed(() => {
  const quantities = {};

  for (const order of cartStore.pendingOrdersList) {
    const items = Array.isArray(order?.items) ? order.items : [];

    for (const item of items) {
      const productId = Number(item?.product);
      if (!productId || Number.isNaN(productId)) {
        continue;
      }

      const currentQty = Number(quantities[productId] || 0);
      quantities[productId] = currentQty + Number(item?.quantity || 0);
    }
  }

  return quantities;
});

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

onMounted(async () => {
  await Promise.allSettled([fetchOffers(), cartStore.syncPendingOrders()]);
});

let searchTimer = null;

function onSearch(value) {
  searchTerm.value = value;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => fetchOffers(value.trim()), 400);
}

function getProducerLabel(product) {
  const producer = product?.producer;

  if (producer && typeof producer === 'object') {
    return producer.name || producer.nome_fantasia || `produtor #${producer.id ?? ''}`;
  }

  if (producer !== undefined && producer !== null) {
    return `produtor #${producer}`;
  }

  return 'produtor';
}

async function handleAddToCart(payload) {
  const product = payload?.product;
  const quantity = Number(payload?.quantity || 0);

  if (!product || quantity <= 0) {
    return;
  }

  addingProductId.value = product.id;

  try {
    await cartStore.addProductToCart(product, quantity);
    const productName = capitalize(product.name || 'Produto');
    const producerLabel = getProducerLabel(product);

    toast.success(`${productName} adicionado ao pedido do ${producerLabel}.`, 'Carrinho atualizado');
  } catch (error) {
    toast.error(
      error?.message || 'Não foi possível adicionar o produto ao carrinho.',
      'Erro ao adicionar',
    );
  } finally {
    addingProductId.value = null;
  }
}
</script>
