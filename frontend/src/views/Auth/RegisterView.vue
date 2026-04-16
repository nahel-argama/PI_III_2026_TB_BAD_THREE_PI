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
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Criar Conta</h2>

      <form @submit.prevent="handleCadastro">
        <div class="mb-4">
          <label class="mb-2 block text-sm font-bold text-gray-700">Nome Completo</label>
          <input
            v-model="form.name"
            type="text"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            required
          />
        </div>

        <div class="mb-4">
          <label class="mb-2 block text-sm font-bold text-gray-700">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            required
          />
        </div>

        <div class="mb-4">
          <label class="mb-2 block text-sm font-bold text-gray-700">Eu sou um:</label>
          <select
            v-model="form.type"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
          >
            <option value="PRODUTOR">Produtor</option>
            <option value="VAREJISTA">Varejista</option>
          </select>
        </div>

        <div class="mb-6">
          <label class="mb-2 block text-sm font-bold text-gray-700">Senha</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            required
          />
        </div>

        <button
          type="submit"
          class="bg-primary hover:bg-secondary w-full rounded-lg px-4 py-2 font-bold text-white transition duration-300"
        >
          Cadastrar
        </button>
        <RouterLink to="/login" class="text-1xl mb-6 text-center text-blue-800">
          Ja tem uma conta?
        </RouterLink>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import api from '../../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = reactive({
  name: '',
  email: '',
  type: 'PRODUTOR',
  password: '',
});

const handleCadastro = async () => {
  try {
    const payload = {
      name: form.name,
      email: form.email,
      type: form.type,
      password: form.password,
    };

    const response = await api.post('/users/', payload);
    alert('Cadastro realizado com sucesso!');
    router.push('/login');
  } catch (error) {
    console.error('Erro no cadastro:', error);
    const backendMessage = error?.response?.data || error?.message || 'Erro desconhecido';
    alert(`Falha ao cadastrar. Detalhes: ${JSON.stringify(backendMessage)}`);
  }
};
</script>
