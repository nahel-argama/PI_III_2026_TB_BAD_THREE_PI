<template>
  <section
    class="flex min-h-[calc(100vh-6.5rem)] w-full items-center justify-center rounded-[28px] border border-dashed border-slate-200/80 bg-white/30 p-6"
  >
    <div class="max-w-xl text-center">
      <p class="text-xs font-bold tracking-[0.28em] text-emerald-600 uppercase">
        {{ eyebrow }}
      </p>
      <h2 class="mt-3 text-3xl font-black tracking-tight text-slate-900">
        {{ title }}
      </h2>
      <p class="mt-3 text-sm leading-7 text-slate-600">
        {{ description }}
      </p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  eyebrow: {
    type: String,
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
});
</script>
