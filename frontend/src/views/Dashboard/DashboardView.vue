<template>
  <DashboardShell
    :sidebar-open="sidebarOpen"
    @close-sidebar="sidebarOpen = false"
  >
    <template #sidebar>
      <DashboardSidebar
        :profile="profile"
        :active-item-id="activeItemId"
        @close-sidebar="sidebarOpen = false"
        @select="handleSelect"
      />
    </template>

    <template #topbar>
      <DashboardTopbar
        :title="profile.title"
        :subtitle="profile.subtitle"
        :role-label="roleLabel"
        :user-name="userName"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
      />
    </template>

    <component :is="activeViewComponent" :role-label="roleLabel" />
  </DashboardShell>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import DashboardShell from '@/components/dashboard/DashboardShell.vue';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar.vue';
import DashboardTopbar from '@/components/dashboard/DashboardTopbar.vue';
import { dashboardProfiles } from '@/data/dashboard';
import StockView from '@/components/dashboard/views/StockView.vue';
import ExploreOffersView from '@/components/dashboard/views/ExploreOffersView.vue';
import WishlistView from '@/components/dashboard/views/WishlistView.vue';
import PurchaseHistoryView from '@/components/dashboard/views/PurchaseHistoryView.vue';
import SalesHistoryView from '@/components/dashboard/views/SalesHistoryView.vue';
import ProfileView from '@/components/dashboard/views/ProfileView.vue';
import ProductImagesPlaceholderView from '@/components/dashboard/views/ProductImagesPlaceholderView.vue';

const authStore = useAuthStore();
const route = useRoute();
const dashboardViewRegistry = {
  PRODUTOR: {
    'meu-estoque': StockView,
    'historico-venda': SalesHistoryView,
    'meu-perfil': ProfileView,
  },
  VAREJISTA: {
    'explorar-ofertas': ExploreOffersView,
    'lista-desejos': WishlistView,
    'historico-compra': PurchaseHistoryView,
    'meu-perfil': ProfileView,
  },
  ADMIN: {
    'gerenciar-imagens-produtos': ProductImagesPlaceholderView,
  },
};

const sidebarOpen = ref(false);
const activeItemId = ref('');

const currentRole = computed(
  () => authStore.getCurrentUserType || authStore.getCurrentUser?.user_type || authStore.getCurrentUser?.type || 'VAREJISTA',
);
const profile = computed(() => dashboardProfiles[currentRole.value] || dashboardProfiles.VAREJISTA);
const defaultActiveItemId = computed(() => profile.value.navItems[0]?.id || '');
const userName = computed(() => authStore.getCurrentUser?.name || 'Usuário Cultiva');
const roleLabel = computed(() => {
  if (currentRole.value === 'PRODUTOR') return 'Produtor';
  if (currentRole.value === 'ADMIN') return 'Administrador';
  return 'Varejista';
});

const activeViewComponent = computed(() => {
  return dashboardViewRegistry[currentRole.value]?.[activeItemId.value] || dashboardViewRegistry[currentRole.value]?.[defaultActiveItemId.value];
});

function hasNavItem(itemId) {
  return profile.value.navItems.some((item) => item.id === itemId);
}

function handleSelect(itemId) {
  activeItemId.value = itemId;
  sidebarOpen.value = false;
}

watch(defaultActiveItemId, (nextDefaultItemId) => {
  if (!hasNavItem(activeItemId.value)) {
    activeItemId.value = nextDefaultItemId;
  }
}, { immediate: true });

watch(
  () => route.query.tab,
  (tabFromQuery) => {
    if (typeof tabFromQuery !== 'string') {
      return;
    }

    if (hasNavItem(tabFromQuery)) {
      activeItemId.value = tabFromQuery;
    }
  },
  { immediate: true },
);
</script>
