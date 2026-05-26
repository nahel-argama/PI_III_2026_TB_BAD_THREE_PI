<template>
  <div class="relative flex min-h-screen items-center justify-center bg-gray-100">
    <RouterLink
      to="/"
      class="absolute top-4 left-4 flex items-center gap-2 rounded-md bg-white/80 px-3 py-2 text-sm font-medium text-slate-700 shadow-md backdrop-blur hover:bg-white"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-4 w-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Voltar
    </RouterLink>

    <div class="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Login</h2>

      <!-- Mensagem de erro -->
      <div v-if="errorMessage" class="mb-4 rounded-lg bg-red-50 p-4">
        <p class="text-center text-sm font-medium text-red-800">{{ errorMessage }}</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="mb-2 block text-sm font-bold text-gray-700">Email</label>
          <input
            v-model="credenciais.email"
            type="email"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            :disabled="isLoading"
            required
          />
        </div>

        <div class="mb-6">
          <label class="mb-2 block text-sm font-bold text-gray-700">Senha</label>
          <input
            v-model="credenciais.senha"
            type="password"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            :disabled="isLoading"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="bg-primary hover:bg-secondary w-full rounded-lg px-4 py-2 font-bold text-white transition duration-300 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ isLoading ? 'Entrando...' : 'Entrar' }}
        </button>

        <div class="mt-4 text-center">
          <RouterLink to="/register" class="text-sm text-blue-800 hover:underline">
            Não possui conta?
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const { login: authLogin } = useAuth();

const isLoading = ref(false);
const credenciais = reactive({
  email: '',
  senha: '',
});

const errorMessage = ref('');

/**
 * Manipulador de login
 *
 * Delega toda lógica de autenticação para o auth store via composable.
 * Este componente cuida apenas de:
 * - UI do formulário
 * - Seu próprio estado de loading e erros
 */
const handleLogin = async () => {
  try {
    errorMessage.value = '';
    isLoading.value = true;

    // Valida campos
    if (!credenciais.email || !credenciais.senha) {
      errorMessage.value = 'Por favor, preencha todos os campos.';
      return;
    }

    // Chama login centralizado (store)
    await authLogin(credenciais.email, credenciais.senha);

    // Se chegou aqui, login foi sucesso
    // Store já salvou token e Pinia está atualizado
    router.push('/dashboard'); // Redireciona para o dashboard adaptativo
  } catch (error) {

    // Trata mensagem de erro do backend
    const msg =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      'Credenciais inválidas. Tente novamente.';

    errorMessage.value = msg;
  } finally {
    isLoading.value = false;
  }
};
</script>
