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
          Cultiva
        </span>
      </div>

      <div class="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
        <a href="#processo" class="transition hover:text-green-600">Como funciona</a>
        <a href="#por-que-escolher" class="transition hover:text-green-600">Por que escolher o cultiva</a>
      </div>

      <div class="flex items-center gap-4">
        <RouterLink
          v-if="auth.isLoggedIn"
          to="/dashboard"
          class="rounded-full bg-green-600 px-6 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-green-700"
        >
          Acessar Dashboard
        </RouterLink>
        <RouterLink
          v-else
          to="/register"
          class="rounded-full bg-green-600 px-6 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-green-700"
        >
          Começar Agora
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuth } from '@/composables/useAuth';

const auth = useAuth();
</script>

<style scoped></style>
