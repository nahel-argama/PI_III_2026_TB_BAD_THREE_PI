<template>
  <nav class="sticky top-0 z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
    <div class="container mx-auto flex h-20 items-center justify-between px-6">
      <button 
        type="button" 
        class="flex w-24 items-center gap-2 text-slate-500 transition hover:text-slate-900" 
        @click="$emit('cancel')"
      >
        <ArrowLeftIcon class="h-5 w-5" />
        <span class="text-sm font-bold">Voltar</span>
      </button>
      <h1 class="text-lg font-black text-slate-900">Finalizar Compra</h1>
      <div class="w-24"></div>
    </div>
  </nav>
</template>

<script setup>
import { ArrowLeftIcon } from '@heroicons/vue/24/outline';
defineEmits(['cancel']);
</script>

<style scoped></style>
