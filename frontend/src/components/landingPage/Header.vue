<template>
  <nav class="sticky top-0 z-50 bg-[#EAF5EC]/90 backdrop-blur-md">
    <div class="container mx-auto flex h-20 items-center justify-between px-6">
      <div class="flex items-center gap-3">
        <img src="/favicon.png" alt="Cultiva" class="h-9 w-9 object-contain" />
        <span class="text-2xl font-black tracking-tight text-slate-900"> Cultiva </span>
      </div>

      <div class="hidden items-center gap-8 text-base font-bold text-slate-800 lg:flex">
        <a href="#como-funciona" class="transition hover:text-[#2CA961]">Como Funciona</a>
        <a href="#beneficios" class="transition hover:text-[#2CA961]">Benefícios</a>
        <a href="#tecnologia" class="transition hover:text-[#2CA961]">Tecnologia</a>
        <a href="#impacto" class="transition hover:text-[#2CA961]">Impacto</a>
      </div>

      <div class="flex items-center gap-4">
        <RouterLink
          v-if="auth.isLoggedIn"
          to="/dashboard"
          class="rounded-full bg-[#2CA961] px-7 py-2.5 text-base font-bold text-white shadow-md transition hover:bg-[#23874d]"
        >
          Acessar Dashboard
        </RouterLink>
        <RouterLink
          v-else
          to="/login"
          class="rounded-full bg-[#2CA961] px-7 py-2.5 text-base font-bold text-white shadow-md transition hover:bg-[#23874d]"
        >
          Acessar Dashboard
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
