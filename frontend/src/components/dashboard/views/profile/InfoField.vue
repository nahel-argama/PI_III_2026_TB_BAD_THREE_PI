<template>
  <div :class="full ? 'md:col-span-2' : ''" class="min-w-0">
    <dt class="text-[11px] font-semibold tracking-[0.16em] text-slate-400 uppercase sm:text-xs">
      {{ label }}
    </dt>
    <dd class="mt-1 text-sm leading-6 font-semibold break-words text-slate-800 sm:text-base">
      {{ value || 'Não informado' }}
    </dd>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    default: null,
  },
  full: {
    type: Boolean,
    default: false,
  },
});
</script>
