<template>
  <section class="space-y-6 pb-6">
    <HistoryToolbar
      eyebrow="Produtor"
      title="Histórico de Venda"
      description="Vendas reais recebidas pelo produtor via pedidos da API."
      :search="searchTerm"
      :item-count="filteredSales.length"
      action-label="vendas"
      @update-search="onSearch"
    />

    <HistoryList
      :items="paginatedSales"
      empty-title="Nenhuma venda encontrada"
      empty-description="Não há pedidos confirmados/cancelados/entregues para exibir."
      item-kind-label="Venda"
    />

    <AppPagination
      v-if="filteredSales.length > 0"
      v-model="currentPage"
      :total-items="filteredSales.length"
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
const sales = ref([]);
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
      note: 'Pedido confirmado pelo varejista.',
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
  const retailerData = order?.retailer_data || {};
  const retailerName = retailerData.trade_name || retailerData.name || `Varejista #${order.retailer}`;
  const retailerDocument = formatDocument(
    retailerData.document_type,
    retailerData.document_number,
  );

  return {
    id: order.id,
    contractCode: `VD-${String(order.id).padStart(6, '0')}`,
    contractTitle: `Pedido #${order.id}`,
    partyName: retailerName,
    partyDocument:
      retailerData.document_type && retailerDocument !== 'Documento não disponível'
        ? `${retailerData.document_type} ${retailerDocument}`
        : retailerDocument,
    partyLocation: formatAddress(retailerData.address),
    partyContact: retailerData.name || retailerName,
    partyEmail: retailerData.email || 'Contato não disponível',
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

async function loadSalesHistory() {
  try {
    const orders = await fetchAllOrders();
    const completedOrders = orders.filter((order) => order?.status !== 'PENDING');

    sales.value = completedOrders
      .map((order) => buildHistoryItem(order))
      .sort((a, b) => b.id - a.id);
  } catch (error) {
    sales.value = [];
    toast.error(error?.message || 'Não foi possível carregar histórico de vendas.', 'Erro');
  }
}

const filteredSales = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return sales.value;
  }

  return sales.value.filter((sale) => {
    return [
      sale.contractCode,
      sale.contractTitle,
      sale.partyName,
      sale.partyContact,
      sale.status,
      sale.date,
      sale.note,
      sale.payment.method,
    ]
      .join(' ')
      .toLowerCase()
      .includes(query);
  });
});

const paginatedSales = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredSales.value.slice(start, end);
});

onMounted(async () => {
  await loadSalesHistory();
});
</script>
