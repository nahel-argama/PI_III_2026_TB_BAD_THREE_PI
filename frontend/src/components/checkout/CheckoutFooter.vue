<template>
  <div class="space-y-4">
    <button
      type="button"
      class="inline-flex w-full items-center justify-center gap-2 rounded-2xl px-8 py-4 text-lg font-black text-white shadow-lg transition-all"
      :class="buttonClass"
      :disabled="disabled"
      @click="$emit('confirm')"
    >
      {{ buttonLabel }}
      <span class="text-xl">→</span>
    </button>
    <p v-if="helperMessage" class="text-center text-xs text-slate-600">{{ helperMessage }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  hasItems: {
    type: Boolean,
    default: true,
  },
});

defineEmits(['confirm']);

const buttonLabel = computed(() => {
  if (props.loading) return 'Confirmando...';
  if (props.readonly) return 'Pedido não editável';
  return 'Finalizar Compra';
});

const helperMessage = computed(() => {
  if (!props.hasItems) return 'Adicione itens ao pedido para confirmar.';
  if (props.readonly) return 'Pedido já confirmado/cancelado. Confirmação bloqueada.';
  return '';
});

const buttonClass = computed(() => {
  if (props.disabled) {
    return 'cursor-not-allowed bg-slate-300 shadow-slate-200';
  }

  return 'bg-green-600 shadow-green-200 hover:-translate-y-1 hover:bg-green-700 active:translate-y-0';
});
</script>

<style scoped></style>
