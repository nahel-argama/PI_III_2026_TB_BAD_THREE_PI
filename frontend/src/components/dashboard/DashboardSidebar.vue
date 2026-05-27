<template>
  <div class="flex h-full flex-col px-5 py-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <img src="/favicon.png" alt="Cultiva" class="h-11 w-11 object-contain" />
        <div>
          <p class="text-[11px] font-bold tracking-[0.28em] text-emerald-500 uppercase">Cultiva</p>
          <p class="text-sm font-semibold text-slate-700">Dashboard</p>
        </div>
      </div>

      <button
        class="rounded-xl border border-slate-200 bg-white p-2 text-slate-600 transition hover:border-emerald-200 hover:text-emerald-600 lg:hidden"
        type="button"
        @click="$emit('close-sidebar')"
      >
        <XMarkIcon class="h-5 w-5" />
      </button>
    </div>

    <nav class="mt-6 space-y-2">
      <button
        v-for="item in profile.navItems"
        :key="item.label"
        type="button"
        class="group flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-semibold text-slate-600 transition hover:bg-emerald-50 hover:text-emerald-700"
        :class="{ 'bg-emerald-50 text-emerald-700': item.id === activeItemId }"
        :aria-current="item.id === activeItemId ? 'page' : undefined"
        @click="$emit('select', item.id)"
      >
        <component
          :is="item.icon"
          class="h-5 w-5 shrink-0 text-slate-400 transition group-hover:text-emerald-500"
          :class="item.id === activeItemId ? 'text-emerald-500' : ''"
        />
        <span>{{ item.label }}</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/24/outline';

defineProps({
  profile: {
    type: Object,
    required: true,
  },
  activeItemId: {
    type: String,
    default: '',
  },
});

defineEmits(['close-sidebar', 'select']);
</script>
