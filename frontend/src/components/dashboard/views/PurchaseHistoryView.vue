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
      @download-invoice="onDownloadInvoice"
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
import { formatDocument, formatPostalCode } from '@/utils/formatters';
import { downloadInvoice } from '@/utils/invoiceGenerator';

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
  const postalCode = address.postal_code ? `CEP ${formatPostalCode(address.postal_code)}` : '';

  return [mainLine, extraLine, postalCode].filter(Boolean).join(' • ') || 'Endereço não disponível';
}



const PAYMENT_METHOD_LABELS = {
  pix: 'PIX',
  invoice: 'Boleto Bancário',
  credit_card: 'Cartão de Crédito',
};

function formatPaymentMethod(method) {
  if (!method) return 'Método não informado';
  return PAYMENT_METHOD_LABELS[method] || method;
}

function getStatusView(status) {
  if (status === 'CONFIRMED') {
    return {
      label: 'Confirmada',
      tone: 'emerald',
    };
  }

  if (status === 'DELIVERED') {
    return {
      label: 'Entregue',
      tone: 'blue',
    };
  }

  if (status === 'CANCELED') {
    return {
      label: 'Cancelada',
      tone: 'red',
    };
  }

  return {
    label: status || 'Desconhecido',
    tone: 'amber',
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
    rawOrder: order,
    contractTitle: `Pedido #${order.id}`,
    partyName: producerName,
    partyDocument:
      producerData.document_type && producerDocument
        ? `${producerData.document_type} ${producerDocument}`
        : producerDocument || 'Documento não disponível',
    partyLocation: formatAddress(producerData.address),
    partyContact: producerData.name || producerName,
    partyEmail: producerData.email || 'Contato não disponível',
    date: formatDate(createdAt),
    status: statusView.label,
    statusTone: statusView.tone,
    payment: {
      method: formatPaymentMethod(order?.payment_method),
      details: order?.payment_method 
        ? (order?.status === 'CANCELED' ? `Tentativa via ${formatPaymentMethod(order.payment_method)}` : `Pago via ${formatPaymentMethod(order.payment_method)}`) 
        : 'Pagamento não registrado.',
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

function onDownloadInvoice(item) {
  downloadInvoice(item.rawOrder);
}

const filteredPurchases = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return purchases.value;
  }

  return purchases.value.filter((purchase) => {
    return [
      purchase.contractTitle,
      purchase.partyName,
      purchase.partyContact,
      purchase.status,
      purchase.date,
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
