<template>
  <div
    class="group relative z-10 rounded-2xl border border-slate-100 bg-white p-10 shadow-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-xl"
  >
    <div
      class="mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-2xl border-4 border-slate-100 bg-gray-100 text-3xl font-black transition-colors"
      :class="themeClasses"
    >
      {{ number }}
    </div>
    <h3 class="mb-4 text-center text-xl font-bold text-slate-900">{{ title }}</h3>
    <p class="text-center text-sm leading-relaxed text-slate-600">
      {{ description }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  number: {
    type: [Number, String],
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  theme: {
    type: String,
    default: 'green',
  },
});

const themeClasses = computed(() => {
  return 'text-green-600 shadow-lg shadow-green-100 group-hover:bg-green-600 group-hover:text-white';
});
</script>
