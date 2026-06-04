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
      @download-invoice="onDownloadInvoice"
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
import { formatDocument, formatPostalCode } from '@/utils/formatters';
import { downloadInvoice } from '@/utils/invoiceGenerator';

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
  const retailerData = order?.retailer_data || {};
  const retailerName =
    retailerData.trade_name || retailerData.name || `Varejista #${order.retailer}`;
  const retailerDocument = formatDocument(retailerData.document_type, retailerData.document_number);

  return {
    id: order.id,
    rawOrder: order,
    contractTitle: `Pedido #${order.id}`,
    partyName: retailerName,
    partyDocument:
      retailerData.document_type && retailerDocument
        ? `${retailerData.document_type} ${retailerDocument}`
        : retailerDocument || 'Documento não disponível',
    partyLocation: formatAddress(retailerData.address),
    partyContact: retailerData.name || retailerName,
    partyEmail: retailerData.email || 'Contato não disponível',
    date: formatDate(createdAt),
    status: statusView.label,
    statusTone: statusView.tone,
    payment: {
      method: formatPaymentMethod(order?.payment_method),
      details: order?.payment_method
        ? order?.status === 'CANCELED'
          ? `Tentativa via ${formatPaymentMethod(order.payment_method)}`
          : `Pago via ${formatPaymentMethod(order.payment_method)}`
        : 'Pagamento não registrado.',
      total: formatMoney(order?.total_value),
    },
    items: items.map((item) => {
      const productId = Number(item?.product);
      const productData = item?.product_data || {};
      return {
        name: productData?.name || `Produto #${productId}`,
        quantity: `${item?.quantity ?? 0} kg`,
        unit: `R$ ${Number(item?.unit_price || 0).toFixed(2)} / kg`,
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

function onDownloadInvoice(item) {
  downloadInvoice(item.rawOrder);
}

const filteredSales = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return sales.value;
  }

  return sales.value.filter((sale) => {
    return [
      sale.contractTitle,
      sale.partyName,
      sale.partyContact,
      sale.status,
      sale.date,
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
