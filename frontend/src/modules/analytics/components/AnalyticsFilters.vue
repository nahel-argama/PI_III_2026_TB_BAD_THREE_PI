<template>
  <div class="flex flex-wrap items-center gap-3">
    <select
      :value="stateFilter"
      class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 focus:outline-none"
      :disabled="isLoading"
      @change="$emit('update:stateFilter', $event.target.value)"
    >
      <option value="">Todos os estados</option>
      <option v-for="uf in estadosOrdenados" :key="uf" :value="uf">
        {{ uf }} {{ uf === userState ? '(Seu Estado)' : '' }}
      </option>
    </select>

    <select
      :value="topFilter"
      class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 focus:outline-none"
      :disabled="isLoading"
      @change="$emit('update:topFilter', Number($event.target.value))"
    >
      <option :value="5">Top 5</option>
      <option :value="10">Top 10</option>
      <option :value="15">Top 15</option>
      <option :value="20">Top 20</option>
    </select>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  stateFilter: { type: String, required: true },
  topFilter: { type: Number, required: true },
  isLoading: { type: Boolean, default: false },
  userState: { type: String, default: '' },
});

defineEmits(['update:stateFilter', 'update:topFilter']);

const estadosBase = [
  'AC',
  'AL',
  'AM',
  'AP',
  'BA',
  'CE',
  'DF',
  'ES',
  'GO',
  'MA',
  'MG',
  'MS',
  'MT',
  'PA',
  'PB',
  'PE',
  'PI',
  'PR',
  'RJ',
  'RN',
  'RO',
  'RR',
  'RS',
  'SC',
  'SE',
  'SP',
  'TO',
];

const estadosOrdenados = computed(() => {
  if (!props.userState) return estadosBase;
  const filtered = estadosBase.filter((e) => e !== props.userState);
  return [props.userState, ...filtered];
});
</script>
