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

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="mb-2 block text-sm font-bold text-gray-700">Email</label>
          <input
            v-model="credenciais.email"
            type="email"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            required
          />
        </div>

        <div class="mb-6">
          <label class="mb-2 block text-sm font-bold text-gray-700">Senha</label>
          <input
            v-model="credenciais.senha"
            type="password"
            class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            required
          />
        </div>

        <button
          type="submit"
          class="bg-primary hover:bg-secondary w-full rounded-lg px-4 py-2 font-bold text-white transition duration-300"
        >
          Entrar
        </button>
        <RouterLink to="/register" class="text-1xl mb-6 text-center text-blue-800">
          Não possui conta?
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

const credenciais = reactive({
  email: '',
  senha: '',
});

//monta o payload legal
const handleLogin = async () => {
  try {
    const payload = {
      email: credenciais.email,
      password: credenciais.senha,
    };

    const response = await api.post('/users/login/', payload);

    const token = response.data?.access;
    if (!token) throw new Error('Token não recebido');

    localStorage.setItem('token', token);

    // Decodifica o payload do JWT para extrair o user_id e buscar o nome do usuário
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          })
          .join(''),
      );
      const payload = JSON.parse(jsonPayload);
      const userId = payload.user_id || payload.userId || payload.id;

      if (userId) {
        const userResp = await api.get(`/users/${userId}/`);
        const userName = userResp.data?.name;
        if (userName) {
          localStorage.setItem('user_name', userName);
          // dispatch para atualizar o header
          window.dispatchEvent(new Event('login'));
        }
      }
    } catch (err) {
      console.warn('Não foi possível buscar nome do usuário após login', err);
    }

    alert('Login bem-sucedido!');
    router.push('/'); // Redireciona para a lanfing
  } catch (error) {
    console.error('Erro no login:', error);
    const msg = error?.response?.data || error?.message || 'Credenciais inválidas.';
    alert(`Erro no login: ${JSON.stringify(msg)}`);
  }
};
</script>
