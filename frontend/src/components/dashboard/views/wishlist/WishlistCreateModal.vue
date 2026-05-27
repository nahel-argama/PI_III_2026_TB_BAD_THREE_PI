<template>
  <Teleport to="body">
    <transition name="wishlist-modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-4 py-6 backdrop-blur-sm"
        @click.self="closeModal"
      >
        <section
          class="w-full max-w-2xl overflow-hidden rounded-[28px] bg-white shadow-[0_24px_80px_rgba(15,23,42,0.22)]"
        >
          <div
            class="flex items-start justify-between gap-4 border-b border-slate-100 px-6 py-5 sm:px-8"
          >
            <div>
              <h3 class="mt-2 text-2xl font-black tracking-tight text-slate-900">
                Adicionar produto
              </h3>
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

          <form class="px-6 pb-6 sm:px-8" @submit.prevent="handleSubmit">
            <AppSelect
              v-model="form.productId"
              label="Nome do produto"
              placeholder="Digite o nome do produto (ex: Feijão)"
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

            <p v-if="submitError" class="mt-2 text-sm text-red-600" role="alert">
              {{ submitError }}
            </p>

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
                :disabled="isSubmitting"
                class="rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-600/25 transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {{ isSubmitting ? 'Salvando…' : 'Salvar produto' }}
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
import { XMarkIcon } from '@heroicons/vue/24/outline';
import AppSelect from '@/components/ui/AppSelect.vue';
import { useProductSearch } from '@/composables/useProductSearch';
import { addProductToWishlist } from '@/services/wishlist';

// ── Props & Emits ────────────────────────────────────────────────────────────

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:modelValue', 'submit']);

// ── Form ─────────────────────────────────────────────────────────────────────

const INITIAL_FORM = { productId: null };
const form = reactive({ ...INITIAL_FORM });

/** Objeto completo da opção selecionada (contém id, name, etc.) */
const selectedProduct = ref(null);

/** Erro retornado pela API ao tentar adicionar */
const submitError = ref('');

const isSubmitting = ref(false);

function resetForm() {
  Object.assign(form, INITIAL_FORM);
  selectedProduct.value = null;
  submitError.value = '';
}

// ── Product Search ────────────────────────────────────────────────────────────

const {
  options: productOptions,
  isLoading: searchLoading,
  search: handleSearch,
  reset: resetSearch,
} = useProductSearch();

// ── Modal Lifecycle ───────────────────────────────────────────────────────────

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      handleSearch();
    } else {
      resetForm();
      resetSearch();
    }
  },
);

// ── Actions ───────────────────────────────────────────────────────────────────

function closeModal() {
  emit('update:modelValue', false);
}

function handleProductSelect(option) {
  selectedProduct.value = option;
}

async function handleSubmit() {
  if (!selectedProduct.value?.id) return;

  submitError.value = '';
  isSubmitting.value = true;

  try {
    const item = await addProductToWishlist(selectedProduct.value.id);
    emit('submit', item);
    closeModal();
  } catch (err) {
    submitError.value =
      err?.response?.data?.detail ?? 'Não foi possível adicionar o produto. Tente novamente.';
  } finally {
    isSubmitting.value = false;
  }
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
