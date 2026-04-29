<template>
  <div
    class="rounded-3xl border border-slate-100 bg-white p-8 shadow-sm transition-shadow hover:shadow-md"
  >
    <div
      class="mb-6 flex h-12 w-12 items-center justify-center rounded-xl bg-green-50 text-green-600"
    >
      <slot name="icon"></slot>
    </div>
    <h3 class="mb-3 text-xl font-bold text-slate-900">{{ title }}</h3>
    <p class="text-sm leading-relaxed text-slate-500">
      {{ description }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  description: String,
});
</script>
