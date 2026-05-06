<template>
  <DashboardShell
    :sidebar-open="sidebarOpen"
    @close-sidebar="sidebarOpen = false"
  >
    <template #sidebar>
      <DashboardSidebar
        :profile="profile"
        @close-sidebar="sidebarOpen = false"
        @navigate="sidebarOpen = false"
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

    <div class="flex min-h-[calc(100vh-6.5rem)] w-full">
      <div class="h-full w-full rounded-[28px] border border-dashed border-slate-200/80 bg-white/30" />
    </div>
  </DashboardShell>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import DashboardShell from '@/components/dashboard/DashboardShell.vue';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar.vue';
import DashboardTopbar from '@/components/dashboard/DashboardTopbar.vue';
import { dashboardProfiles } from '@/data/dashboard';

const authStore = useAuthStore();

const sidebarOpen = ref(false);

const currentRole = computed(() => authStore.getCurrentUserType || authStore.getCurrentUser?.type || 'VAREJISTA');
const profile = computed(() => dashboardProfiles[currentRole.value] || dashboardProfiles.VAREJISTA);
const userName = computed(() => authStore.getCurrentUser?.name || 'Usuário Cultiva');
const roleLabel = computed(() => (currentRole.value === 'PRODUTOR' ? 'Produtor' : 'Varejista'));
</script>
