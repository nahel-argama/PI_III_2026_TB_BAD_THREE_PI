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

const authStore = useAuthStore();

const sidebarOpen = ref(false);
const activeItemId = ref('');

const currentRole = computed(() => authStore.getCurrentUserType || authStore.getCurrentUser?.type || 'VAREJISTA');
const profile = computed(() => dashboardProfiles[currentRole.value] || dashboardProfiles.VAREJISTA);
const userName = computed(() => authStore.getCurrentUser?.name || 'Usuário Cultiva');
const roleLabel = computed(() => (currentRole.value === 'PRODUTOR' ? 'Produtor' : 'Varejista'));

const activeViewComponent = computed(() => {
  const viewMap = {
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
  };

  return viewMap[currentRole.value]?.[activeItemId.value] || viewMap[currentRole.value]?.[profile.value.navItems[0]?.id];
});

function handleSelect(itemId) {
  activeItemId.value = itemId;
  sidebarOpen.value = false;
}

watch(
  profile,
  (nextProfile) => {
    activeItemId.value = nextProfile.navItems[0]?.id || '';
  },
  { immediate: true },
);
</script>
