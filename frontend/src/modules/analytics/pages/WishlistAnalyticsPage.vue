<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Análise de Produtos</h1>
        <p class="text-sm text-slate-500">Produtos mais desejados pelos varejistas</p>
      </div>
      
      <AnalyticsFilters
        v-model:stateFilter="stateFilter"
        v-model:topFilter="topFilter"
        :is-loading="isLoading"
        :user-state="userState"
      />
    </div>
    
    <!-- Erro -->
    <div v-if="error" class="rounded-xl bg-red-50 p-4 text-sm text-red-600">
      <p class="font-semibold">Não foi possível carregar os dados.</p>
      <p>{{ error }}</p>
    </div>
    
    <AnalyticsSummaryCards :data="data" :is-loading="isLoading" />
    
    <!-- Tabs -->
    <div class="rounded-2xl border border-slate-100 bg-white shadow-sm overflow-hidden">
      <div class="flex border-b border-slate-100">
        <button
          @click="activeTab = 'ranking'"
          class="px-6 py-4 text-sm font-semibold transition"
          :class="activeTab === 'ranking' ? 'border-b-2 border-emerald-500 text-emerald-600' : 'text-slate-500 hover:bg-slate-50'"
        >
          Ranking
        </button>
        <button
          @click="activeTab = 'grafico'"
          class="px-6 py-4 text-sm font-semibold transition"
          :class="activeTab === 'grafico' ? 'border-b-2 border-emerald-500 text-emerald-600' : 'text-slate-500 hover:bg-slate-50'"
        >
          Gráfico
        </button>
      </div>
      
      <div class="p-6">
        <!-- Skeleton Loading -->
        <div v-if="isLoading" class="space-y-4">
          <div v-for="i in 5" :key="i" class="h-12 bg-slate-100 animate-pulse rounded-xl"></div>
        </div>
        
        <!-- Empty State -->
        <EmptyState v-else-if="!data?.results?.length" />
        
        <!-- Ranking Tab -->
        <WishlistRankingTable v-else-if="activeTab === 'ranking'" :results="data.results" />
        
        <!-- Gráfico Tab -->
        <WishlistPieChart v-else-if="activeTab === 'grafico'" :results="data.results" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useWishlistAnalytics } from '../hooks/useWishlistAnalytics';
import AnalyticsFilters from '../components/AnalyticsFilters.vue';
import AnalyticsSummaryCards from '../components/AnalyticsSummaryCards.vue';
import WishlistRankingTable from '../components/WishlistRankingTable.vue';
import WishlistPieChart from '../components/WishlistPieChart.vue';
import EmptyState from '../components/EmptyState.vue';

const activeTab = ref('ranking');

const {
  stateFilter,
  topFilter,
  data,
  isLoading,
  error,
  userState,
  fetchAnalytics,
} = useWishlistAnalytics();
</script>
