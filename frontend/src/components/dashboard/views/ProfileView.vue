<template>
  <DashboardPlaceholderView
    :eyebrow="roleLabel"
    title="Meu Perfil"
    description="Componente de teste compartilhado para validar a área de perfil."
  />
</template>

<script setup>
import DashboardPlaceholderView from '@/components/dashboard/views/DashboardPlaceholderView.vue';

defineProps({
  roleLabel: {
  type: String,
  required: true,
  },
});
</script>
