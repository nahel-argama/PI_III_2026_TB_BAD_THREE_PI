<template>
  <Teleport to="body">
    <transition name="product-images-modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-4 py-6 backdrop-blur-sm"
        @click.self="closeModal"
      >
        <section class="w-full max-w-2xl overflow-hidden rounded-[28px] bg-white shadow-[0_24px_80px_rgba(15,23,42,0.22)]">
          <div class="flex items-start justify-between gap-4 border-b border-slate-100 px-6 py-5 sm:px-8">
            <div>
              <p class="text-xs font-bold uppercase tracking-[0.28em] text-emerald-600">
                Gerenciar Imagens
              </p>
              <h3 class="mt-2 text-2xl font-black tracking-tight text-slate-900">
                {{ mode === 'edit' ? 'Editar produto' : 'Adicionar produto' }}
              </h3>
              <p class="mt-2 text-sm leading-6 text-slate-600">
                Cadastre o nome e a imagem do produto de forma totalmente mockada.
              </p>
            </div>

            <button
              type="button"
              class="rounded-2xl border border-slate-200 bg-white p-2.5 text-slate-500 transition hover:border-slate-300 hover:text-slate-700"
              aria-label="Fechar modal"
              @click="closeModal"
            >
              <XMarkIcon class="h-5 w-5" />
            </button>
          </div>

          <form class="px-6 py-6 sm:px-8" @submit.prevent="handleSubmit">
            <div class="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
              <div class="space-y-6">
                <label class="space-y-2">
                  <span class="text-sm font-semibold text-slate-700">Nome do produto</span>
                  <input
                    v-model="form.name"
                    type="text"
                    :readonly="mode === 'edit'"
                    class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-300 focus:bg-white focus:ring-4 focus:ring-emerald-100"
                    :class="mode === 'edit' ? 'cursor-not-allowed bg-slate-100 text-slate-500 focus:border-slate-200 focus:bg-slate-100 focus:ring-0' : ''"
                    placeholder="Ex.: Tomate Italiano"
                    required
                  />
                </label>

                <ProductImageUploader
                  v-model="form.imageUrl"
                  label="Subir arquivo"
                />
              </div>

              <div class="space-y-3">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <p class="text-xs font-bold uppercase tracking-[0.28em] text-emerald-600">
                      Prévia
                    </p>
                    <h4 class="mt-2 text-xl font-black tracking-tight text-slate-900">
                      Imagem selecionada
                    </h4>
                  </div>
                </div>

                <div class="overflow-hidden rounded-[24px] border border-dashed border-slate-200 bg-slate-50">
                  <div class="flex aspect-[4/3] items-center justify-center bg-white">
                    <img
                      v-if="form.imageUrl"
                      :src="form.imageUrl"
                      alt="Prévia da imagem do produto"
                      class="h-full w-full object-cover"
                    />
                    <div v-else class="text-center text-slate-400">
                      <PhotoIcon class="mx-auto h-10 w-10" />
                      <p class="mt-3 text-sm font-semibold text-slate-500">
                        Nenhuma imagem selecionada
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <button
                type="button"
                class="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
                @click="closeModal"
              >
                Cancelar
              </button>

              <button
                type="submit"
                class="rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-600/25 transition hover:bg-emerald-700"
              >
                {{ mode === 'edit' ? 'Salvar alterações' : 'Salvar produto' }}
              </button>
            </div>
          </form>
        </section>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { reactive, watch } from 'vue';
import { PhotoIcon, XMarkIcon } from '@heroicons/vue/24/outline';
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
  name: '',
  imageUrl: '',
});

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      form.name = props.initialValue?.name || '';
      form.imageUrl = props.initialValue?.imageUrl || '';
      return;
    }

    resetForm();
  },
);

function resetForm() {
  form.name = '';
  form.imageUrl = '';
}

function closeModal() {
  emit('update:modelValue', false);
}

function handleSubmit() {
  emit('submit', {
    name: form.name,
    imageUrl: form.imageUrl,
  });
  closeModal();
}
</script>

<style scoped>
.product-images-modal-enter-active,
.product-images-modal-leave-active {
  transition: opacity 0.2s ease;
}

.product-images-modal-enter-from,
.product-images-modal-leave-to {
  opacity: 0;
}
</style>
