<template>
  <section class="space-y-6 pb-6">
    <header
      class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6"
    >
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p class="text-xs font-bold tracking-[0.28em] text-emerald-600 uppercase">Produtor</p>
          <h2 class="mt-2 text-3xl font-black tracking-tight text-slate-900">
            Análise de Produtos
          </h2>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            Produtos mais desejados pelos varejistas
          </p>
        </div>

        <div class="flex w-full flex-col gap-3 sm:flex-row sm:items-center lg:w-auto">
          <AnalyticsFilters
            v-model:stateFilter="stateFilter"
            v-model:topFilter="topFilter"
            :is-loading="isLoading"
            :user-state="userState"
          />
        </div>
      </div>
    </header>

    <!-- Erro -->
    <div
      v-if="error"
      class="rounded-[28px] border border-red-100 bg-red-50 p-6 text-sm text-red-600 shadow-sm"
    >
      <p class="text-lg font-semibold">Não foi possível carregar os dados.</p>
      <p class="mt-1">{{ error }}</p>
    </div>

    <AnalyticsSummaryCards :data="data" :is-loading="isLoading" />

    <template v-if="!isLoading && data?.results?.length">
      <div
        class="overflow-hidden rounded-[28px] border border-white/70 bg-white/90 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur"
      >
        <div class="flex border-b border-slate-100">
          <button
            class="px-6 py-4 text-sm font-semibold transition"
            :class="
              activeTab === 'ranking'
                ? 'border-b-2 border-emerald-500 text-emerald-600'
                : 'text-slate-500 hover:bg-slate-50'
            "
            @click="activeTab = 'ranking'"
          >
            Lista de Ranking
          </button>
          <button
            class="px-6 py-4 text-sm font-semibold transition"
            :class="
              activeTab === 'grafico'
                ? 'border-b-2 border-emerald-500 text-emerald-600'
                : 'text-slate-500 hover:bg-slate-50'
            "
            @click="activeTab = 'grafico'"
          >
            Gráfico de Distribuição
          </button>
        </div>

        <div>
          <WishlistRankingList v-if="activeTab === 'ranking'" :results="data.results" />
          <div v-else-if="activeTab === 'grafico'" class="p-6">
            <WishlistPieChart :results="data.results" />
          </div>
        </div>
      </div>
    </template>

    <div v-else-if="isLoading" class="space-y-4">
      <div v-for="i in 5" :key="i" class="h-16 animate-pulse rounded-[16px] bg-slate-100"></div>
    </div>

    <EmptyState v-else />
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { useWishlistAnalytics } from '../hooks/useWishlistAnalytics';
import AnalyticsFilters from '../components/AnalyticsFilters.vue';
import AnalyticsSummaryCards from '../components/AnalyticsSummaryCards.vue';
import WishlistRankingList from '../components/WishlistRankingList.vue';
import WishlistPieChart from '../components/WishlistPieChart.vue';
import EmptyState from '../components/EmptyState.vue';

const activeTab = ref('ranking');

const { stateFilter, topFilter, data, isLoading, error, userState } = useWishlistAnalytics();
</script>
