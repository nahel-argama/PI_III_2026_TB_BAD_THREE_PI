<template>
  <section class="space-y-6 pb-6">
    <HistoryToolbar
      eyebrow="Produtor"
      title="Histórico de Venda"
      description="Visualização mockada das vendas registradas pelo produtor, em uma lista expansível."
      :search="searchTerm"
      :item-count="filteredSales.length"
      action-label="vendas"
      @update-search="searchTerm = $event"
    />

    <HistoryList
      :items="filteredSales"
      empty-title="Nenhuma venda encontrada"
      empty-description="Tente outro termo de busca ou altere os mocks desta aba."
      item-kind-label="Venda"
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import HistoryList from './history/HistoryList.vue';
import HistoryToolbar from './history/HistoryToolbar.vue';

const searchTerm = ref('');

const salesHistory = ref([
  {
    id: 1,
    contractCode: 'VD-2026-001',
    contractTitle: 'Venda de Tomate Italiano',
    partyName: 'Mercado Central',
    partyDocument: 'CNPJ 12.345.678/0001-90',
    partyLocation: 'Campinas - SP',
    partyContact: 'Renato Silva',
    partyEmail: 'renato@mercadocentral.com.br',
    date: '07/05/2026',
    status: 'Concluída',
    note: 'Lote enviado no período da manhã',
    validity: 'até 12/05/2026',
    statusTone: 'emerald',
    payment: {
      method: 'PIX à vista',
      details: 'Pagamento confirmado no fechamento do contrato',
      total: 'R$ 8.420,00',
    },
    items: [
      { name: 'Tomate Italiano', quantity: '180 kg', unit: 'caixa', category: 'Hortaliças' },
      { name: 'Molho de manjericão', quantity: '30 unidades', unit: 'maço', category: 'Ervas' },
    ],
  },
  {
    id: 2,
    contractCode: 'VD-2026-002',
    contractTitle: 'Venda de Alface Crespa',
    partyName: 'Hortifruti Aurora',
    partyDocument: 'CNPJ 23.456.789/0001-11',
    partyLocation: 'Sorocaba - SP',
    partyContact: 'Marina Costa',
    partyEmail: 'marina@hortifruti.com.br',
    date: '05/05/2026',
    status: 'Em negociação',
    note: 'Aguardando confirmação do comprador',
    validity: 'até 10/05/2026',
    statusTone: 'amber',
    payment: {
      method: 'Boleto faturado',
      details: 'Condição de 14 dias para liquidação',
      total: 'R$ 2.130,00',
    },
    items: [
      { name: 'Alface Crespa', quantity: '95 molhos', unit: 'molho', category: 'Folhosas' },
    ],
  },
  {
    id: 3,
    contractCode: 'VD-2026-003',
    contractTitle: 'Venda de Banana Prata',
    partyName: 'Supermercado Rio Verde',
    partyDocument: 'CNPJ 34.567.890/0001-22',
    partyLocation: 'Itu - SP',
    partyContact: 'Clara Mendes',
    partyEmail: 'compras@rioverde.com.br',
    date: '02/05/2026',
    status: 'Concluída',
    note: 'Venda recorrente do mês',
    validity: 'até 09/05/2026',
    statusTone: 'emerald',
    payment: {
      method: 'Transferência bancária',
      details: 'Liquidação em 2 parcelas',
      total: 'R$ 5.860,00',
    },
    items: [
      { name: 'Banana Prata', quantity: '210 kg', unit: 'caixa', category: 'Frutas' },
    ],
  },
  {
    id: 4,
    contractCode: 'VD-2026-004',
    contractTitle: 'Venda de Cenoura Extra',
    partyName: 'Distribuidora Serra',
    partyDocument: 'CNPJ 45.678.901/0001-33',
    partyLocation: 'Jundiaí - SP',
    partyContact: 'Paulo Nunes',
    partyEmail: 'paulo@distribuidoraserra.com.br',
    date: '29/04/2026',
    status: 'Cancelada',
    note: 'Pedido cancelado antes do faturamento',
    validity: 'sem validade ativa',
    statusTone: 'red',
    payment: {
      method: 'Sem pagamento',
      details: 'Contrato cancelado antes da cobrança',
      total: 'R$ 0,00',
    },
    items: [
      { name: 'Cenoura Extra', quantity: '130 kg', unit: 'saco', category: 'Hortaliças' },
    ],
  },
]);

const filteredSales = computed(() => {
  const query = searchTerm.value.trim().toLowerCase();

  if (!query) {
    return salesHistory.value;
  }

  return salesHistory.value.filter((sale) => {
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
</script>
