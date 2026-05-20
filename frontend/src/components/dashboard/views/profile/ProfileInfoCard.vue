<template>
  <div
    class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6"
  >
    <!-- Cabeçalho do card -->
    <div class="mb-5 flex items-center gap-3">
      <div
        class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
      >
        <component :is="icon" class="h-5 w-5" />
      </div>
      <h3 class="text-base font-bold text-slate-800">{{ title }}</h3>
    </div>

    <!-- Grid de campos -->
    <dl class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div
        v-for="field in fields"
        :key="field.label"
        :class="field.full ? 'sm:col-span-2' : ''"
        class="flex flex-col gap-1"
      >
        <dt class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          {{ field.label }}
        </dt>
        <dd class="text-sm font-semibold text-slate-800">
          {{ field.value || '—' }}
        </dd>
      </div>
    </dl>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  icon: {
    type: [Object, Function],
    required: true,
  },
  fields: {
    type: Array,
    required: true,
    // [{ label: String, value: String, full?: Boolean }]
  },
});
</script>
