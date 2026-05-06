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

    <component :is="activeViewComponent" />
  </DashboardShell>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import DashboardShell from '@/components/dashboard/DashboardShell.vue';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar.vue';
import DashboardTopbar from '@/components/dashboard/DashboardTopbar.vue';
import { dashboardProfiles } from '@/data/dashboard';
import ProducerTest1View from '@/components/dashboard/views/ProducerTest1View.vue';
import ProducerTest2View from '@/components/dashboard/views/ProducerTest2View.vue';
import ProducerTest3View from '@/components/dashboard/views/ProducerTest3View.vue';
import RetailerTest1View from '@/components/dashboard/views/RetailerTest1View.vue';
import RetailerTest2View from '@/components/dashboard/views/RetailerTest2View.vue';
import RetailerTest3View from '@/components/dashboard/views/RetailerTest3View.vue';

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
      'prod-teste-1': ProducerTest1View,
      'prod-teste-2': ProducerTest2View,
      'prod-teste-3': ProducerTest3View,
    },
    VAREJISTA: {
      'varet-teste-1': RetailerTest1View,
      'varet-teste-2': RetailerTest2View,
      'varet-teste-3': RetailerTest3View,
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
