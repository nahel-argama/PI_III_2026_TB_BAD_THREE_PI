<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount } from 'vue';
import { useAuth } from '@/composables/useAuth';

/**
 * Inicializa autenticação quando a aplicação é montada
 *
 * Responsabilidades:
 * - Carrega token de localStorage
 * - Restaura estado de autenticação do Pinia
 * - Permite que componentes filhos acessem estado de auth imediatamente
 */
const { authStore } = useAuth();

onBeforeMount(async () => {
  try {
    // Carrega token do localStorage e restaura estado
    await authStore.initializeAuth();
  } catch (err) {
    console.error('Erro ao inicializar autenticação:', err);
    // Mesmo com erro, continua - usuário pode fazer login novamente
  }
});
</script>

<style scoped></style>
