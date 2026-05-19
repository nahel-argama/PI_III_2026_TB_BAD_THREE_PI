<template>
  <Teleport to="body">
    <transition name="product-images-modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm transition-all duration-300"
        @click.self="closeModal"
      >
        <section
          class="relative w-full max-w-2xl overflow-hidden rounded-3xl bg-white border border-slate-100 shadow-[0_20px_60px_-10px_rgba(15,23,42,0.18)]"
        >
          <!-- Top Decorative Gradient Bar -->
          <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600"></div>

          <!-- Header -->
          <div class="flex items-center justify-between gap-3 border-b border-slate-100/80 px-5 py-4">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 ring-2 ring-emerald-50/50 shadow-sm">
                <SparklesIcon class="h-5 w-5" />
              </div>
              <div>
                <h3 class="text-lg font-extrabold tracking-tight text-slate-900 leading-none">
                  {{ mode === 'edit' ? 'Editar Imagem' : 'Vincular Imagem' }}
                </h3>
                <p class="text-[11px] text-slate-500 leading-none mt-1">
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
                  :disabled="mode === 'edit'"
                  @search="handleSearch"
                  @select="handleProductSelect"
                />
              </div>

              <!-- Divider -->
              <div class="border-t border-slate-100"></div>

              <!-- Section 2: Horizontal File Upload -->
              <div>
                <ProductImageUploader v-model="form.imageUrl" label="Arquivo de Imagem" />
              </div>

              <!-- Section 3: Clean Raw Preview underneath the uploader -->
              <div v-if="form.imageUrl" class="space-y-1.5 pt-1 animate-fade-in">
                <label class="block text-xs font-bold tracking-wider text-slate-500 uppercase">
                  Prévia
                </label>
                
                <div class="overflow-hidden rounded-xl border border-slate-200 bg-slate-50 h-64 flex items-center justify-center p-1">
                  <img
                    :src="form.imageUrl"
                    alt="Prévia"
                    class="h-full w-full object-contain rounded-lg"
                  />
                </div>
              </div>

            </div>

            <!-- Footer Buttons -->
            <div class="mt-6 flex gap-3 justify-end border-t border-slate-100 pt-4">
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
import { useProductSearch } from '@/composables/useProductSearch';
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
  (isOpen) => {
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
}

function closeModal() {
  emit('update:modelValue', false);
}

function handleProductSelect(option) {
  selectedProduct.value = option;
  form.name = option?.name || '';
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
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
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
