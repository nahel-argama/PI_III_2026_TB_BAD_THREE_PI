<template>
  <Teleport to="body">
    <transition name="wishlist-modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-4 py-6 backdrop-blur-sm"
        @click.self="closeModal"
      >
        <section class="w-full max-w-2xl overflow-hidden rounded-[28px] bg-white shadow-[0_24px_80px_rgba(15,23,42,0.22)]">
          <div class="flex items-start justify-between gap-4 border-b border-slate-100 px-6 py-5 sm:px-8">
            <div>
              <p class="text-xs font-bold uppercase tracking-[0.28em] text-emerald-600">
                Marketplace
              </p>
              <h3 class="mt-2 text-2xl font-black tracking-tight text-slate-900">
                Adicionar produto
              </h3>
              <p class="mt-2 text-sm leading-6 text-slate-600">
                Cadastro local e mockado apenas com o nome do produto.
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
            <label class="space-y-2">
              <span class="text-sm font-semibold text-slate-700">Nome do produto</span>
              <input
                v-model="form.name"
                type="text"
                class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-300 focus:bg-white focus:ring-4 focus:ring-emerald-100"
                placeholder="Ex.: Abacate premium"
                required
              />
            </label>

            <div class="mt-6 rounded-[24px] border border-dashed border-slate-200 bg-slate-50 px-5 py-8 text-center">
              <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm">
                <PhotoIcon class="h-8 w-8" />
              </div>
              <p class="mt-3 text-sm font-semibold text-slate-600">
                Foto do produto ficará aqui no futuro
              </p>
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
                Salvar produto
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

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:modelValue', 'submit']);

const initialForm = {
  name: '',
};

const form = reactive({ ...initialForm });

watch(
  () => props.modelValue,
  (isOpen) => {
    if (!isOpen) {
      resetForm();
    }
  },
);

function resetForm() {
  Object.assign(form, initialForm);
}

function closeModal() {
  emit('update:modelValue', false);
}

function handleSubmit() {
  emit('submit', { ...form });
  closeModal();
}
</script>

<style scoped>
.wishlist-modal-enter-active,
.wishlist-modal-leave-active {
  transition: opacity 0.2s ease;
}

.wishlist-modal-enter-from,
.wishlist-modal-leave-to {
  opacity: 0;
}
</style>
