<template>
  <div class="relative w-full h-full overflow-hidden flex items-center justify-center bg-slate-50">
    <!-- Loading State -->
    <div
      v-if="loading"
      class="absolute inset-0 flex items-center justify-center bg-slate-100/80 backdrop-blur-[1px] transition-opacity duration-300"
    >
      <div class="relative flex items-center justify-center">
        <!-- Elegant Premium Spinner -->
        <svg
          class="animate-spin h-8 w-8 text-emerald-600"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="3"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      </div>
    </div>

    <!-- Error/No Image Fallback -->
    <div
      v-else-if="error || !src"
      class="flex flex-col items-center justify-center gap-2 h-full w-full bg-slate-100 text-slate-400"
    >
      <PhotoIcon class="h-10 w-10 stroke-[1.5]" />
      <span v-if="error" class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
        Erro ao carregar
      </span>
    </div>

    <!-- Real Image -->
    <img
      v-else
      :src="displayUrl"
      :alt="alt"
      class="h-full w-full transition-all duration-300"
      :class="[
        objectFitClass,
        imageLoading ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
      ]"
      @load="onImageLoad"
      @error="onImageError"
    />
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';
import { PhotoIcon } from '@heroicons/vue/24/outline';
import api from '@/services/api';

const props = defineProps({
  src: {
    type: String,
    default: '',
  },
  alt: {
    type: String,
    default: 'Imagem',
  },
  objectFitClass: {
    type: String,
    default: 'object-cover',
  },
});

const displayUrl = ref('');
const loading = ref(false);
const imageLoading = ref(true);
const error = ref(false);

let currentObjectUrl = '';

function cleanUp() {
  if (currentObjectUrl) {
    try {
      URL.revokeObjectURL(currentObjectUrl);
    } catch {
      // Ignora erro ao revogar
    }
    currentObjectUrl = '';
  }
}

async function loadSecureImage(url) {
  cleanUp();
  error.value = false;
  imageLoading.value = true;

  if (!url) {
    displayUrl.value = '';
    return;
  }

  // Se for uma imagem local base64/dataURL, exibe diretamente
  if (url.startsWith('data:')) {
    displayUrl.value = url;
    imageLoading.value = false;
    return;
  }

  loading.value = true;

  try {
    const response = await api.get(url, {
      responseType: 'blob',
    });

    const blob = response.data;
    currentObjectUrl = URL.createObjectURL(blob);
    displayUrl.value = currentObjectUrl;
  } catch {
    error.value = true;
    displayUrl.value = '';
  } finally {
    loading.value = false;
  }
}

function onImageLoad() {
  imageLoading.value = false;
}

function onImageError() {
  error.value = true;
}

watch(
  () => props.src,
  (newSrc) => {
    loadSecureImage(newSrc);
  },
  { immediate: true }
);

onBeforeUnmount(() => {
  cleanUp();
});
</script>
