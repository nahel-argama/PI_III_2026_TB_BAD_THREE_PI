<template>
  <section class="space-y-6 pb-6">
    <HistoryToolbar
      eyebrow="Varejista"
      title="Histórico de Compra"
      description="Lista mockada das compras do varejista, em uma lista expansível."
      :search="searchTerm"
      :item-count="filteredPurchases.length"
      action-label="compras"
      @update-search="searchTerm = $event"
    />

    <HistoryList
      :items="filteredPurchases"
      empty-title="Nenhuma compra encontrada"
      empty-description="Tente outro termo de busca ou altere os mocks desta aba."
      item-kind-label="Compra"
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import HistoryList from './history/HistoryList.vue';
import HistoryToolbar from './history/HistoryToolbar.vue';

const searchTerm = ref('');

const purchaseHistory = ref([
  {
    id: 1,
    contractCode: 'CP-2026-011',
    contractTitle: 'Compra de Tomate Italiano',
    partyName: 'Sítio Boa Vista',
    partyDocument: 'CPF/CNPJ 123.456.789-00',
    partyLocation: 'Valinhos - SP',
    partyContact: 'Sérgio Martins',
    partyEmail: 'sergio@sitioboavista.com.br',
    date: '07/05/2026',
    status: 'Recebida',
    note: 'Entrega confirmada e conferida no estoque',
    validity: 'até 08/05/2026',
    statusTone: 'emerald',
    payment: {
      method: 'PIX na entrega',
      details: 'Pagamento feito após conferência dos volumes',
      total: 'R$ 8.420,00',
    },
    items: [
      { name: 'Tomate Italiano', quantity: '180 kg', unit: 'caixa', category: 'Hortaliças' },
      { name: 'Manjericão fresco', quantity: '30 unidades', unit: 'maço', category: 'Ervas' },
    ],
  },
  {
    id: 2,
    contractCode: 'CP-2026-012',
    contractTitle: 'Compra de Maçã Gala',
    partyName: 'Cooperativa Serra Fresca',
    partyDocument: 'CNPJ 234.567.890/0001-00',
    partyLocation: 'Limeira - SP',
    partyContact: 'Camila Rocha',
    partyEmail: 'camila@serrafresca.com.br',
    date: '04/05/2026',
    status: 'Em trânsito',
    note: 'Saiu para entrega no início da tarde',
    validity: 'até 09/05/2026',
    statusTone: 'blue',
    payment: {
      method: 'Boleto faturado',
      details: 'Liquidação prevista em 14 dias',
      total: 'R$ 6.150,00',
    },
    items: [
      { name: 'Maçã Gala', quantity: '240 kg', unit: 'fardo', category: 'Frutas' },
    ],
  },
  {
    id: 3,
    contractCode: 'CP-2026-013',
    contractTitle: 'Compra de Cenoura Extra',
    partyName: 'Fazenda Horizonte',
    partyDocument: 'CPF/CNPJ 345.678.901-11',
    partyLocation: 'Itatiba - SP',
    partyContact: 'Aline Prado',
    partyEmail: 'aline@fazendahorizonte.com.br',
    date: '01/05/2026',
    status: 'Recebida',
    note: 'Compra concluída sem pendências',
    validity: 'até 03/05/2026',
    statusTone: 'emerald',
    payment: {
      method: 'Transferência bancária',
      details: 'Pagamento em duas parcelas',
      total: 'R$ 4.280,00',
    },
    items: [
      { name: 'Cenoura Extra', quantity: '130 kg', unit: 'saco', category: 'Hortaliças' },
    ],
  },
  {
    id: 4,
    contractCode: 'CP-2026-014',
    contractTitle: 'Compra de Banana Prata',
    partyName: 'Rancho Vale Verde',
    partyDocument: 'CPF/CNPJ 456.789.012-22',
    partyLocation: 'Mogi Mirim - SP',
    partyContact: 'Thiago Alves',
    partyEmail: 'thiago@valeverde.com.br',
    date: '29/04/2026',
    status: 'Pendente',
    note: 'Aguardando confirmação final',
    validity: 'até 06/05/2026',
    statusTone: 'amber',
    payment: {
      method: 'Cartão faturado',
      details: 'Compra aprovada aguardando emissão',
      total: 'R$ 5.860,00',
    },
    items: [
      { name: 'Banana Prata', quantity: '210 kg', unit: 'caixa', category: 'Frutas' },
    ],
  },
]);

const filteredPurchases = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return purchaseHistory.value;
  }

  return purchaseHistory.value.filter((purchase) => {
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
</script>
