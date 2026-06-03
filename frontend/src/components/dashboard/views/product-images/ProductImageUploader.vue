<template>
  <div class="space-y-2">
    <label v-if="label" class="block text-xs font-bold tracking-wider text-slate-500 uppercase">
      {{ label }}
    </label>

    <input ref="inputRef" type="file" accept="image/*" class="hidden" @change="handleChange" />

    <!-- Horizontal Input Design -->
    <div
      class="flex w-full items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50/80 p-2 transition duration-200 hover:border-emerald-400 hover:bg-emerald-50/10"
    >
      <button
        type="button"
        class="flex shrink-0 items-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-xs font-bold text-white transition hover:bg-slate-800 active:scale-[0.97]"
        @click="inputRef?.click()"
      >
        <ArrowUpTrayIcon class="h-4 w-4" />
        <span>{{ modelValue ? 'Trocar Imagem' : 'Escolher Arquivo' }}</span>
      </button>

      <div class="flex min-w-0 flex-1 items-center justify-between px-2">
        <div class="flex min-w-0 items-center gap-2">
          <PhotoIcon
            class="h-4 w-4 shrink-0"
            :class="modelValue ? 'text-emerald-500' : 'text-slate-400'"
          />
          <span
            class="truncate text-xs"
            :class="modelValue ? 'font-bold text-slate-700' : 'font-medium text-slate-400'"
          >
            {{ fileName || 'Nenhum arquivo selecionado' }}
          </span>
        </div>

        <span
          v-if="fileExtension"
          class="shrink-0 rounded-md bg-emerald-100 px-2 py-0.5 text-[10px] font-black tracking-wider text-emerald-700 uppercase"
        >
          {{ fileExtension }}
        </span>
        <span
          v-else
          class="shrink-0 rounded-md bg-slate-200/60 px-1.5 py-0.5 text-[9px] font-bold tracking-wider text-slate-400 uppercase"
        >
          Sem Mídia
        </span>
      </div>

      <!-- Clear Button if file selected -->
      <button
        v-if="modelValue"
        type="button"
        class="shrink-0 rounded-lg p-1.5 text-slate-400 transition hover:bg-rose-50 hover:text-rose-500"
        title="Remover imagem"
        @click="clearFile"
      >
        <XMarkIcon class="h-4 w-4" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { ArrowUpTrayIcon, PhotoIcon, XMarkIcon } from '@heroicons/vue/24/outline';

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

const fileName = ref('');
const fileExtension = ref('');

watch(
  () => props.modelValue,
  (nextValue) => {
    if (nextValue) {
      if (nextValue.startsWith('data:image/')) {
        // Extract from base64 MIME type if possible
        const mimeMatch = nextValue.match(/data:(image\/[a-zA-Z+]+);base64,/);
        const mime = mimeMatch ? mimeMatch[1] : 'image/png';
        fileExtension.value = mime.split('/')[1] || 'png';
        if (!fileName.value) {
          fileName.value = 'nova_imagem';
        }
      } else {
        // Extract from URL
        try {
          let cleanUrl = nextValue.split('?')[0].split('#')[0];
          if (cleanUrl.endsWith('/')) {
            cleanUrl = cleanUrl.slice(0, -1);
          }
          const lastPart = cleanUrl.substring(cleanUrl.lastIndexOf('/') + 1) || 'imagem';
          const dotParts = lastPart.split('.');
          if (dotParts.length > 1) {
            fileExtension.value = dotParts.pop().toLowerCase();
            fileName.value = dotParts.join('.');
          } else {
            fileName.value = lastPart;
            fileExtension.value = 'png';
          }
        } catch {
          fileName.value = 'imagem_vinculada';
          fileExtension.value = 'png';
        }
      }
    } else {
      fileName.value = '';
      fileExtension.value = '';
    }
  },
  { immediate: true },
);

function handleChange(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  // Store name and extension from file object
  const dotParts = file.name.split('.');
  if (dotParts.length > 1) {
    fileExtension.value = dotParts.pop().toLowerCase();
    fileName.value = dotParts.join('.');
  } else {
    fileName.value = file.name;
    fileExtension.value = 'png';
  }

  const reader = new FileReader();
  reader.onload = () => {
    emit('update:modelValue', String(reader.result || ''));
  };
  reader.readAsDataURL(file);
}

function clearFile() {
  fileName.value = '';
  fileExtension.value = '';
  if (inputRef.value) {
    inputRef.value.value = '';
  }
  emit('update:modelValue', '');
}
</script>

<style scoped></style>
