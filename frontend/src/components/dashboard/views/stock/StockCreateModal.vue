<template>
  <Teleport to="body">
    <transition name="stock-modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-4 py-6 backdrop-blur-sm"
        @click.self="closeModal"
      >
        <section
          class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-[28px] bg-white shadow-[0_24px_80px_rgba(15,23,42,0.22)]"
        >
          <div
            class="flex items-start justify-between gap-4 border-b border-slate-100 px-6 py-5 sm:px-8"
          >
            <div>
              <h3 class="mt-2 text-2xl font-black tracking-tight text-slate-900">
                Adicionar Produto
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

          <form class="flex flex-col gap-4 px-6 py-6 sm:px-8" @submit.prevent="handleSubmit">
            <div>
              <AppSelect
                v-model="form.external_id"
                label="Nome do Produto"
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

              <div
                v-if="isLoadingPrice"
                class="mt-1.5 flex items-center gap-2 text-xs font-medium text-slate-500"
              >
                <svg
                  class="h-3.5 w-3.5 animate-spin text-emerald-600"
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
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <span>Buscando preço sugerido na sua região...</span>
              </div>
              <p v-else-if="suggestedPrice" class="mt-1.5 text-xs font-medium text-slate-500">
                Preço sugerido na sua região:
                <span class="font-bold text-emerald-600">{{
                  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(
                    suggestedPrice,
                  )
                }}</span>
              </p>
            </div>

            <AppSelect
              v-model="form.category"
              label="Categoria"
              placeholder="Selecione uma categoria"
              :options="categoryOptions"
              label-key="name"
              value-key="id"
              required
            />

            <div>
              <label for="price" class="mb-2 block text-sm font-bold text-slate-700">Preço</label>
              <input
                id="price"
                v-model.number="form.price"
                type="number"
                step="0.01"
                min="0.01"
                required
                class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
              />
            </div>

            <div>
              <label for="total_quantity" class="mb-2 block text-sm font-bold text-slate-700"
                >Quantidade Total</label
              >
              <input
                id="total_quantity"
                v-model.number="form.total_quantity"
                type="number"
                min="1"
                required
                class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
              />
            </div>

            <div>
              <label for="description" class="mb-2 block text-sm font-bold text-slate-700"
                >Descrição (Opcional)</label
              >
              <textarea
                id="description"
                v-model="form.description"
                rows="3"
                class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
              ></textarea>
            </div>

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
import { createProduct } from '@/services/product';
import { listCategories } from '@/services/category';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:modelValue', 'submit']);

const INITIAL_FORM = {
  external_id: null,
  category: null,
  price: '',
  total_quantity: '',
  description: '',
};
const form = reactive({ ...INITIAL_FORM });

const selectedProduct = ref(null);
const submitError = ref('');
const isSubmitting = ref(false);
const suggestedPrice = ref(null);
const isLoadingPrice = ref(false);

const categoryOptions = ref([]);

const authStore = useAuthStore();

function resetForm() {
  Object.assign(form, INITIAL_FORM);
  selectedProduct.value = null;
  submitError.value = '';
  suggestedPrice.value = null;
  isLoadingPrice.value = false;
}

const {
  options: productOptions,
  isLoading: searchLoading,
  search: handleSearch,
  reset: resetSearch,
} = useProductSearch();

async function fetchCategories() {
  if (categoryOptions.value.length > 0) return;
  try {
    const data = await listCategories();
    categoryOptions.value = data.results || data;
  } catch {
    // Silencia o erro
  }
}

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      fetchCategories();
    } else {
      resetForm();
      resetSearch();
    }
  },
);

function closeModal() {
  emit('update:modelValue', false);
}

async function handleProductSelect(option) {
  selectedProduct.value = option;
  form.external_id = option?.id || null;
  suggestedPrice.value = null;

  if (option?.id) {
    isLoadingPrice.value = true;
    try {
      const userState = authStore.getCurrentUser?.state;
      const stateParam = userState ? userState.toLowerCase() : 'sp';
      const todayDate = new Date().toISOString().split('T')[0];

      const response = await fetch(
        `http://localhost:8001/api/products/${option.id}/prices?from_date=2020-01-01&to_date=${todayDate}&state=${stateParam}`,
      );

      if (response.ok) {
        const data = await response.json();
        const price =
          data.avg_price ||
          data.average_price ||
          data.price ||
          (Array.isArray(data) && data[0]?.price);
        if (price) {
          suggestedPrice.value = price;
        }
      }
    } catch (err) {
      console.error('Erro ao buscar preços:', err);
    } finally {
      isLoadingPrice.value = false;
    }
  }
}

async function handleSubmit() {
  if (!form.external_id || !form.category || !form.price || !form.total_quantity) return;

  submitError.value = '';
  isSubmitting.value = true;

  try {
    const data = {
      external_id: form.external_id,
      category: form.category,
      price: form.price,
      total_quantity: form.total_quantity,
      reserved_quantity: 0,
      description: form.description || '',
    };

    const item = await createProduct(data);
    emit('submit', item);
    closeModal();
  } catch (err) {
    submitError.value =
      err?.response?.data?.detail ?? 'Não foi possível adicionar o produto. Verifique os dados.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
.stock-modal-enter-active,
.stock-modal-leave-active {
  transition: opacity 0.2s ease;
}

.stock-modal-enter-from,
.stock-modal-leave-to {
  opacity: 0;
}
</style>
