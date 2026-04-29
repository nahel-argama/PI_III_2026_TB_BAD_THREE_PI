<template>
  <nav class="sticky top-0 z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
    <div class="container mx-auto flex h-20 items-center justify-between px-6">
      <div class="flex items-center gap-2">
        <div
          class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-600 text-xl font-bold text-white"
        >
          π
        </div>
        <span class="text-xl font-extrabold tracking-tight text-slate-900">
          Culti<span class="text-2xl text-green-600">va</span>
        </span>
      </div>

      <div class="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
        <a href="#como-funciona" class="transition hover:text-green-600">Como Funciona</a>
        <a href="#produtores" class="transition hover:text-green-600">Para Produtores</a>
        <a href="#varejo" class="transition hover:text-green-600">Para o Varejo</a>
        <a href="#precos" class="transition hover:text-green-600">Preços Justos</a>
      </div>

      <div class="flex items-center gap-4">
        <div ref="menuRef" class="relative">
          <button
            v-if="userName"
            @click="toggleMenu"
            class="hidden items-center gap-3 rounded-full px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 md:inline-flex"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-green-600"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M10 2a4 4 0 100 8 4 4 0 000-8zM2 18a8 8 0 1116 0H2z" />
            </svg>
            <span class="text-sm font-medium text-slate-700">Olá, {{ userName }}</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 text-slate-500"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M5.23 7.21a.75.75 0 011.06.02L10 11.293l3.71-4.06a.75.75 0 111.14.98l-4.25 4.656a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
          <RouterLink
            to="/register"
            v-else
            class="rounded-full bg-green-600 px-6 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-green-700"
          >
            Começar Agora
          </RouterLink>

          <div
            v-if="showMenu"
            class="ring-opacity-5 absolute right-0 mt-2 min-w-40 overflow-hidden rounded-lg border border-slate-100 bg-white shadow-md"
          >
            <div class="py-1">
              <button
                @click="handleLogout"
                class="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-slate-700 transition-colors hover:bg-slate-100"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 text-red-500"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M3 4.5A1.5 1.5 0 014.5 3h7a1.5 1.5 0 010 3H9v8.25A1.75 1.75 0 017.25 16h-2.5A1.75 1.75 0 013 14.25V4.5zM13 7.5a.75.75 0 00-.75.75v6a.75.75 0 001.5 0v-6A.75.75 0 0013 7.5z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span>Sair</span>
              </button>
            </div>
          </div>
        </div>

        <button class="p-2 text-slate-600 md:hidden">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const userName = ref(localStorage.getItem('user_name'));
const showMenu = ref(false);
const menuRef = ref(null);

function updateUserName() {
  userName.value = localStorage.getItem('user_name');
}

function toggleMenu() {
  showMenu.value = !showMenu.value;
}

function onDocumentClick(e) {
  if (!menuRef.value) return;
  const el = menuRef.value;
  if (el.contains(e.target)) return;
  showMenu.value = false;
}

async function handleLogout() {
  // limpa os dados de login e tals
  localStorage.removeItem('token');
  localStorage.removeItem('user_name');
  window.dispatchEvent(new Event('logout'));
  updateUserName();
  showMenu.value = false;
  router.push('/');
}

onMounted(() => {
  window.addEventListener('login', updateUserName);
  window.addEventListener('storage', updateUserName);
  document.addEventListener('click', onDocumentClick);
});

onUnmounted(() => {
  window.removeEventListener('login', updateUserName);
  window.removeEventListener('storage', updateUserName);
  document.removeEventListener('click', onDocumentClick);
});
</script>
