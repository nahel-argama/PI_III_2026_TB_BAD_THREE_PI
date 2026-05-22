<template>
  <section class="space-y-6 pb-6">
    <HistoryToolbar
      eyebrow="Varejista"
      title="Histórico de Compra"
      description="Compras reais feitas pelo varejista via pedidos da API."
      :search="searchTerm"
      :item-count="filteredPurchases.length"
      action-label="compras"
      @update-search="onSearch"
    />

    <HistoryList
      :items="paginatedPurchases"
      empty-title="Nenhuma compra encontrada"
      empty-description="Não há pedidos confirmados/cancelados/entregues para exibir."
      item-kind-label="Compra"
    />

    <AppPagination
      v-if="filteredPurchases.length > 0"
      v-model="currentPage"
      :total-items="filteredPurchases.length"
      :items-per-page="itemsPerPage"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import HistoryList from './history/HistoryList.vue';
import HistoryToolbar from './history/HistoryToolbar.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import { listOrders } from '@/services/ordersService';
import { useToast } from '@/composables/useToast';

const searchTerm = ref('');
const purchases = ref([]);
const currentPage = ref(1);
const itemsPerPage = 10;
const toast = useToast();

function onSearch(value) {
  searchTerm.value = value;
  currentPage.value = 1;
}

function formatDate(value) {
  if (!value) return '-';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return '-';
  return new Intl.DateTimeFormat('pt-BR').format(parsed);
}

function formatMoney(value) {
  const amount = Number(value || 0);
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(amount);
}

function formatAddress(address) {
  if (!address) return 'Endereço não disponível';

  const mainLine = [address.street, address.number].filter(Boolean).join(', ');
  const extraLine = [address.neighborhood, address.city, address.state].filter(Boolean).join(' • ');
  const postalCode = address.postal_code ? `CEP ${address.postal_code}` : '';

  return [mainLine, extraLine, postalCode].filter(Boolean).join(' • ') || 'Endereço não disponível';
}

function formatDocument(documentType, documentNumber) {
  const digits = String(documentNumber || '').replace(/\D/g, '');

  if (!digits) {
    return 'Documento não disponível';
  }

  if (documentType === 'CPF' && digits.length === 11) {
    return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  }

  if (documentType === 'CNPJ' && digits.length === 14) {
    return digits.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  }

  return documentNumber;
}

function getStatusView(status) {
  if (status === 'CONFIRMED') {
    return {
      label: 'Confirmada',
      tone: 'emerald',
      note: 'Pedido confirmado com sucesso.',
    };
  }

  if (status === 'DELIVERED') {
    return {
      label: 'Entregue',
      tone: 'blue',
      note: 'Pedido entregue ao varejista.',
    };
  }

  if (status === 'CANCELED') {
    return {
      label: 'Cancelada',
      tone: 'red',
      note: 'Pedido cancelado.',
    };
  }

  return {
    label: status || 'Desconhecido',
    tone: 'amber',
    note: 'Status em atualização.',
  };
}

async function fetchAllOrders() {
  const allOrders = [];
  let currentPage = 1;
  let hasNextPage = true;

  while (hasNextPage) {
    const payload = await listOrders({ page: currentPage });
    const pageOrders = Array.isArray(payload) ? payload : (payload?.results ?? []);
    allOrders.push(...pageOrders);

    if (Array.isArray(payload)) {
      hasNextPage = false;
      continue;
    }

    hasNextPage = Boolean(payload?.next);
    currentPage += 1;
  }

  return allOrders;
}

function buildHistoryItem(order) {
  const statusView = getStatusView(order?.status);
  const createdAt = order?.created_at;
  const items = Array.isArray(order?.items) ? order.items : [];
  const producerData = order?.producer_data || {};
  const producerName = producerData.trade_name || producerData.name || `Produtor #${order.producer}`;
  const producerDocument = formatDocument(
    producerData.document_type,
    producerData.document_number,
  );

  return {
    id: order.id,
    contractCode: `CP-${String(order.id).padStart(6, '0')}`,
    contractTitle: `Pedido #${order.id}`,
    partyName: producerName,
    partyDocument:
      producerData.document_type && producerDocument !== 'Documento não disponível'
        ? `${producerData.document_type} ${producerDocument}`
        : producerDocument,
    partyLocation: formatAddress(producerData.address),
    partyContact: producerData.name || producerName,
    partyEmail: producerData.email || 'Contato não disponível',
    date: formatDate(createdAt),
    status: statusView.label,
    note: statusView.note,
    validity: '-',
    statusTone: statusView.tone,
    payment: {
      method: 'Método não informado',
      details: 'Dados de pagamento não retornados pela API de pedidos.',
      total: formatMoney(order?.total_value),
    },
    items: items.map((item) => {
      const productId = Number(item?.product);
      const productData = item?.product_data || {};
      return {
        name: productData?.name || `Produto #${productId}`,
        quantity: String(item?.quantity ?? 0),
        unit: `R$ ${Number(item?.unit_price || 0).toFixed(2)} un.`,
        category: productData?.category_name || 'Sem categoria',
      };
    }),
  };
}

async function loadPurchaseHistory() {
  try {
    const orders = await fetchAllOrders();
    const completedOrders = orders.filter((order) => order?.status !== 'PENDING');

    purchases.value = completedOrders
      .map((order) => buildHistoryItem(order))
      .sort((a, b) => b.id - a.id);
  } catch (error) {
    purchases.value = [];
    toast.error(error?.message || 'Não foi possível carregar histórico de compras.', 'Erro');
  }
}

const filteredPurchases = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return purchases.value;
  }

  return purchases.value.filter((purchase) => {
    return [
      purchase.contractCode,
      purchase.contractTitle,
      purchase.partyName,
      purchase.partyContact,
      purchase.status,
      purchase.date,
      purchase.note,
      purchase.payment.method,
    ]
      .join(' ')
      .toLowerCase()
      .includes(query);
  });
});

const paginatedPurchases = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredPurchases.value.slice(start, end);
});

onMounted(async () => {
  await loadPurchaseHistory();
});
</script>
