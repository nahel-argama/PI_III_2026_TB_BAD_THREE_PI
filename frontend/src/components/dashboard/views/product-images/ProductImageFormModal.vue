<template>
  <Teleport to="body">
    <transition name="product-images-modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm transition-all duration-300"
        @click.self="closeModal"
      >
        <section
          class="relative w-full max-w-2xl overflow-hidden rounded-3xl border border-slate-100 bg-white shadow-[0_20px_60px_-10px_rgba(15,23,42,0.18)]"
        >
          <!-- Top Decorative Gradient Bar -->
          <div
            class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600"
          ></div>

          <!-- Header -->
          <div
            class="flex items-center justify-between gap-3 border-b border-slate-100/80 px-5 py-4"
          >
            <div class="flex items-center gap-3">
              <div
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 shadow-sm ring-2 ring-emerald-50/50"
              >
                <SparklesIcon class="h-5 w-5" />
              </div>
              <div>
                <h3 class="text-lg leading-none font-extrabold tracking-tight text-slate-900">
                  {{ mode === 'edit' ? 'Editar Imagem' : 'Vincular Imagem' }}
                </h3>
                <p class="mt-1 text-[11px] leading-none text-slate-500">
                  Defina a imagem padrão do produto.
                </p>
              </div>
            </div>

            <button
              type="button"
              class="rounded-xl border border-slate-200 bg-white p-2 text-slate-400 transition hover:border-slate-300 hover:text-slate-700 hover:shadow-sm focus:outline-none"
              aria-label="Fechar modal"
              @click="closeModal"
            >
              <XMarkIcon class="h-4 w-4" />
            </button>
          </div>

          <!-- Form Content -->
          <form class="px-5 py-4" @submit.prevent="handleSubmit">
            <div class="space-y-4">
              <!-- Section 1: Product Selection -->
              <div>
                <AppSelect
                  v-model="form.productId"
                  label="Produto"
                  placeholder="Selecione o produto..."
                  :options="productOptions"
                  label-key="name"
                  value-key="id"
                  :loading="searchLoading"
                  :filter-locally="false"
                  autocomplete
                  required
                  @search="handleSearch"
                  @select="handleProductSelect"
                />
              </div>

              <!-- Divider -->
              <div class="border-t border-slate-100"></div>

              <!-- Section 2: Horizontal File Upload -->
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <label class="block text-xs font-bold tracking-wider text-slate-500 uppercase">
                    Arquivo de Imagem
                  </label>

                  <!-- Small AI Generation Button next to the label -->
                  <button
                    v-if="aiFeatureAvailable && form.productId"
                    type="button"
                    :disabled="isGenerating"
                    class="inline-flex items-center gap-1.5 rounded-lg bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600 px-3 py-1 text-[10px] font-black uppercase tracking-wider text-white shadow-md shadow-emerald-500/20 transition duration-300 hover:from-emerald-600 hover:to-teal-600 hover:shadow-emerald-500/30 hover:scale-[1.03] active:scale-[0.97] disabled:opacity-75 disabled:cursor-not-allowed"
                    @click="handleGenerateAiImage"
                  >
                    <svg v-if="isGenerating" class="h-3 w-3 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>{{ isGenerating ? 'Gerando...' : 'Gerar com IA' }}</span>
                  </button>
                </div>

                <ProductImageUploader v-model="form.imageUrl" label="" />
              </div>

              <!-- Section 3: Clean Raw Preview underneath the uploader -->
              <div v-if="form.imageUrl" class="animate-fade-in space-y-1.5 pt-1">
                <label class="block text-xs font-bold tracking-wider text-slate-500 uppercase">
                  Prévia
                </label>

                <div
                  class="flex h-64 items-center justify-center overflow-hidden rounded-xl border border-slate-200 bg-slate-50 p-1"
                >
                  <AppSecureImage
                    :src="form.imageUrl"
                    alt="Prévia"
                    object-fit-class="object-contain rounded-lg"
                  />
                </div>
              </div>
            </div>

            <!-- Footer Buttons -->
            <div class="mt-6 flex justify-end gap-3 border-t border-slate-100 pt-4">
              <button
                type="button"
                class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-bold text-slate-600 transition hover:border-slate-300 hover:bg-slate-50 hover:text-slate-800 active:scale-[0.98]"
                @click="closeModal"
              >
                Cancelar
              </button>

              <button
                type="submit"
                class="inline-flex items-center justify-center gap-1.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 px-5 py-2 text-xs font-extrabold text-white shadow-md shadow-emerald-600/10 transition hover:from-emerald-700 hover:to-teal-700 hover:shadow-lg active:scale-[0.98]"
              >
                <span>Salvar</span>
              </button>
            </div>
          </form>
        </section>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';
import { XMarkIcon, SparklesIcon } from '@heroicons/vue/24/outline';
import AppSelect from '@/components/ui/AppSelect.vue';
import AppSecureImage from '@/components/ui/AppSecureImage.vue';
import { useProductSearch } from '@/composables/useProductSearch';
import { checkAiGenerationFeature, generateDefaultProductImage } from '@/services/defaultProductImages';
import { useToast } from '@/composables/useToast';
import ProductImageUploader from './ProductImageUploader.vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  mode: {
    type: String,
    default: 'create',
  },
  initialValue: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['update:modelValue', 'submit']);

const toast = useToast();
const aiFeatureAvailable = ref(false);
const isGenerating = ref(false);

const form = reactive({
  productId: null,
  name: '',
  imageUrl: '',
});

const selectedProduct = ref(null);

const {
  options: productOptions,
  isLoading: searchLoading,
  search: handleSearch,
  reset: resetSearch,
} = useProductSearch();

watch(
  () => props.modelValue,
  async (isOpen) => {
    if (isOpen) {
      if (props.mode === 'edit') {
        form.productId = props.initialValue?.product_external_key || '';
        form.name = props.initialValue?.name || '';
        productOptions.value = [
          {
            id: form.productId,
            name: form.name,
          },
        ];
        selectedProduct.value = {
          id: form.productId,
          name: form.name,
        };
      } else {
        handleSearch();
      }
      form.imageUrl = props.initialValue?.imageUrl || '';

      try {
        aiFeatureAvailable.value = await checkAiGenerationFeature();
      } catch {
        aiFeatureAvailable.value = false;
      }
      return;
    }

    resetForm();
    resetSearch();
  },
);

function resetForm() {
  form.productId = null;
  form.name = '';
  form.imageUrl = '';
  selectedProduct.value = null;
  aiFeatureAvailable.value = false;
  isGenerating.value = false;
}

function closeModal() {
  emit('update:modelValue', false);
}

function handleProductSelect(option) {
  selectedProduct.value = option;
  form.name = option?.name || '';
  form.imageUrl = '';
}

async function handleGenerateAiImage() {
  if (!form.productId) return;
  isGenerating.value = true;
  try {
    const blob = await generateDefaultProductImage(form.productId);
    const reader = new FileReader();
    reader.onloadend = () => {
      form.imageUrl = reader.result;
      toast.success('Imagem gerada com sucesso!', 'IA Concluída');
    };
    reader.onerror = () => {
      toast.error('Erro ao ler a imagem gerada.', 'Geração por IA');
    };
    reader.readAsDataURL(blob);
  } catch (error) {
    const status = error?.response?.status;
    if (status === 503) {
      toast.error('Geração por IA indisponível no momento (desativada no backend).', 'Recurso Indisponível');
    } else if (status === 429) {
      toast.error('Limite de gerações atingido. Tente novamente em instantes.', 'Limite Excedido');
    } else {
      toast.error('Não foi possível gerar a imagem. Verifique as credenciais ou tente novamente.', 'Falha na IA');
    }
  } finally {
    isGenerating.value = false;
  }
}

function handleSubmit() {
  emit('submit', {
    productId: form.productId,
    imageUrl: form.imageUrl,
  });
  closeModal();
}
</script>

<style scoped>
.product-images-modal-enter-active,
.product-images-modal-leave-active {
  transition: opacity 0.25s ease;
}

.product-images-modal-enter-from,
.product-images-modal-leave-to {
  opacity: 0;
}

.product-images-modal-enter-active section,
.product-images-modal-leave-active section {
  transition:
    transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 0.25s ease;
}

.product-images-modal-enter-from section,
.product-images-modal-leave-to section {
  transform: scale(0.97) translateY(8px);
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
