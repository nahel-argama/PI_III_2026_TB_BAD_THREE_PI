<template>
  <div class="flex w-full flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
    <div class="flex items-start gap-3">
      <button
        class="rounded-2xl border border-slate-200 bg-white p-3 text-slate-700 shadow-sm transition hover:border-emerald-200 hover:text-emerald-600 lg:hidden"
        type="button"
        @click="$emit('toggle-sidebar')"
      >
        <Bars3Icon class="h-5 w-5" />
      </button>

      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-600">
          {{ roleLabel }}
        </p>
        <h1 class="mt-1 text-2xl font-black tracking-tight text-slate-900 sm:text-3xl">
          {{ title }}
        </h1>
        <p class="mt-1 max-w-2xl text-sm leading-6 text-slate-600">
          {{ subtitle }}
        </p>
      </div>
    </div>

    <div ref="menuRef" class="relative flex items-center justify-end gap-2 sm:gap-3">
      <button
        class="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-emerald-200 hover:bg-emerald-50"
        type="button"
        @click="toggleMenu"
      >
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-100 text-emerald-700">
          <UserCircleIcon class="h-5 w-5" />
        </div>
        <span class="hidden sm:inline">{{ userName }}</span>
        <ChevronDownIcon class="h-4 w-4 text-slate-400" />
      </button>

      <div
        v-if="showMenu"
        class="absolute right-0 top-full z-30 mt-2 min-w-44 overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-lg"
      >
        <button
          type="button"
          class="flex w-full items-center gap-3 px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-50 hover:text-red-600"
          @click="handleLogout"
        >
          <ArrowRightOnRectangleIcon class="h-4 w-4 text-red-500" />
          <span>Deslogar</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  ChevronDownIcon,
  UserCircleIcon,
} from '@heroicons/vue/24/outline';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const auth = useAuth();
const showMenu = ref(false);
const menuRef = ref(null);

function toggleMenu() {
  showMenu.value = !showMenu.value;
}

function onDocumentClick(event) {
  if (!menuRef.value) return;

  if (menuRef.value.contains(event.target)) {
    return;
  }

  showMenu.value = false;
}

async function handleLogout() {
  try {
    await auth.logout();
    showMenu.value = false;
    await router.push('/login');
  } catch (error) {
    console.error('Erro ao deslogar:', error);
    showMenu.value = false;
    await router.push('/login');
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick);
});

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick);
});

defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: true,
  },
  roleLabel: {
    type: String,
    required: true,
  },
  userName: {
    type: String,
    required: true,
  },
});

defineEmits(['toggle-sidebar']);
</script>
