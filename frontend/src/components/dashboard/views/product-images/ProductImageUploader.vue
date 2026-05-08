<template>
  <div class="space-y-3">
    <label class="block text-sm font-semibold text-slate-700">
      {{ label }}
    </label>

    <input
      ref="inputRef"
      type="file"
      accept="image/*"
      class="hidden"
      @change="handleChange"
    />

    <button
      type="button"
      class="flex w-full flex-col items-center justify-center gap-3 rounded-[24px] border border-dashed border-slate-200 bg-slate-50 px-6 py-8 text-center transition hover:border-emerald-300 hover:bg-emerald-50/60"
      @click="inputRef?.click()"
    >
      <div
        class="flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm"
      >
        <ArrowUpTrayIcon class="h-7 w-7" />
      </div>

      <div>
        <p class="text-sm font-semibold text-slate-700">
          {{ fileLabel }}
        </p>
        <p class="mt-1 text-xs leading-5 text-slate-500">
          JPG, PNG ou WebP.
        </p>
      </div>
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { ArrowUpTrayIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: 'Imagem do produto',
  },
});

const emit = defineEmits(['update:modelValue']);
const inputRef = ref(null);
const previewUrl = ref('');
const fileLabel = ref('Subir imagem');

watch(
  () => props.modelValue,
  (nextValue) => {
    previewUrl.value = nextValue;
    fileLabel.value = nextValue ? 'Trocar imagem' : 'Subir imagem';
  },
  { immediate: true },
);

function handleChange(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    previewUrl.value = String(reader.result || '');
    emit('update:modelValue', previewUrl.value);
    fileLabel.value = 'Trocar imagem';
  };
  reader.readAsDataURL(file);
}
</script>
