<template>
  <header
    class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6"
  >
    <div class="flex items-center gap-4">
        <div
          class="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-400 to-emerald-600 text-2xl font-black text-white shadow-lg shadow-emerald-500/30"
        >
          {{ initials }}
        </div>

        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-600">
            {{ roleLabel }}
          </p>
          <h2 class="mt-0.5 text-2xl font-black tracking-tight text-slate-900">
            {{ name }}
          </h2>
          <p class="mt-0.5 text-sm text-slate-500">{{ email }}</p>
        </div>
      </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  name: {
    type: String,
    default: '',
  },
  email: {
    type: String,
    default: '',
  },
  roleLabel: {
    type: String,
    default: '',
  },
});

const initials = computed(() => {
  if (!props.name) return '?';
  return props.name
    .trim()
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0].toUpperCase())
    .join('');
});
</script>
