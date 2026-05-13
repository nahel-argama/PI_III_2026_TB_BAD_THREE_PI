<template>
  <nav
    v-if="!hideOnSinglePage || totalPages > 1"
    class="app-pagination"
    :class="[`app-pagination--${size}`]"
    aria-label="Paginação"
  >
    <!-- Results Info -->
    <div v-if="showInfo" class="app-pagination__info">
      <span class="app-pagination__info-text">
        Exibindo
        <span>{{ itemsOnPage }}</span>
        itens de
        <span>{{ totalItems }}</span>
        encontrados
      </span>
    </div>

    <!-- Controls -->
    <div class="app-pagination__controls">
      <!-- Previous Button -->
      <button
        type="button"
        class="app-pagination__btn app-pagination__btn--prev"
        :disabled="modelValue <= 1"
        aria-label="Página anterior"
        @click="changePage(modelValue - 1)"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20" aria-hidden="true">
          <path
            fill-rule="evenodd"
            d="M11.78 5.22a.75.75 0 0 1 0 1.06L8.06 10l3.72 3.72a.75.75 0 1 1-1.06 1.06l-4.25-4.25a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z"
            clip-rule="evenodd"
          />
        </svg>
      </button>

      <!-- Page Numbers -->
      <div class="app-pagination__pages">
        <template v-for="(page, index) in paginationRange" :key="index">
          <button
            v-if="typeof page === 'number'"
            type="button"
            class="app-pagination__page-btn"
            :class="{ 'app-pagination__page-btn--active': page === modelValue }"
            :aria-current="page === modelValue ? 'page' : undefined"
            :aria-label="`Ir para página ${page}`"
            @click="changePage(page)"
          >
            {{ page }}
          </button>
          <span v-else class="app-pagination__ellipsis" aria-hidden="true">
            {{ page }}
          </span>
        </template>
      </div>

      <!-- Next Button -->
      <button
        type="button"
        class="app-pagination__btn app-pagination__btn--next"
        :disabled="modelValue >= totalPages"
        aria-label="Próxima página"
        @click="changePage(modelValue + 1)"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20" aria-hidden="true">
          <path
            fill-rule="evenodd"
            d="M8.22 5.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L11.94 10 8.22 6.28a.75.75 0 0 1 0-1.06Z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  /** Página atual (v-model) */
  modelValue: {
    type: Number,
    default: 1,
  },
  /** Total de itens */
  totalItems: {
    type: Number,
    default: 0,
  },
  /** Itens por página */
  itemsPerPage: {
    type: Number,
    default: 20,
  },
  /** Quantidade máxima de botões de página visíveis */
  maxVisibleButtons: {
    type: Number,
    default: 5,
  },
  /** Exibe o texto de informações (Exibindo X-Y de Z) */
  showInfo: {
    type: Boolean,
    default: true,
  },
  /** Oculta o componente se houver apenas uma página */
  hideOnSinglePage: {
    type: Boolean,
    default: false,
  },
  /** Tamanho do componente: 'sm' | 'md' | 'lg' */
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
});

const emit = defineEmits(['update:modelValue', 'change']);

// ─── Computed ────────────────────────────────────────────────────────────────

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.totalItems / props.itemsPerPage));
});

const startItem = computed(() => {
  if (props.totalItems === 0) return 0;
  return (props.modelValue - 1) * props.itemsPerPage + 1;
});

const endItem = computed(() => {
  return Math.min(props.modelValue * props.itemsPerPage, props.totalItems);
});

const itemsOnPage = computed(() => {
  if (props.totalItems === 0) return 0;
  return endItem.value - startItem.value + 1;
});

/**
 * Gera o array de páginas com elipses (ex: [1, '...', 4, 5, 6, '...', 10])
 */
const paginationRange = computed(() => {
  const total = totalPages.value;
  const current = props.modelValue;
  const maxButtons = props.maxVisibleButtons;

  if (total <= maxButtons) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  const range = [];
  const sideButtons = Math.floor((maxButtons - 3) / 2); // Excluindo 1, total e elipses

  // Sempre inclui a primeira página
  range.push(1);

  let start = Math.max(2, current - sideButtons);
  let end = Math.min(total - 1, current + sideButtons);

  // Ajuste se estiver perto do início ou fim
  if (current <= sideButtons + 1) {
    end = maxButtons - 2;
  } else if (current >= total - sideButtons) {
    start = total - (maxButtons - 3);
  }

  // Adiciona elipse inicial se necessário
  if (start > 2) {
    range.push('...');
  } else if (start === 2) {
    // Evita elipse para apenas um número
  }

  // Adiciona números do meio
  for (let i = start; i <= end; i++) {
    range.push(i);
  }

  // Adiciona elipse final se necessário
  if (end < total - 1) {
    range.push('...');
  }

  // Sempre inclui a última página
  if (total > 1) {
    range.push(total);
  }

  return range;
});

// ─── Methods ─────────────────────────────────────────────────────────────────

function changePage(page) {
  if (page < 1 || page > totalPages.value || page === props.modelValue) return;
  emit('update:modelValue', page);
  emit('change', page);
}
</script>

<style scoped>
.app-pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

@media (min-width: 640px) {
  .app-pagination {
    flex-direction: row;
    justify-content: space-between;
  }
}

/* ── Info ────────────────────────────────────────────────────────────────── */
.app-pagination__info {
  font-size: 0.875rem;
  color: #6b7280; /* gray-500 */
}

.app-pagination__info-number {
  font-weight: 600;
  color: #111827; /* gray-900 */
}

/* ── Controls ────────────────────────────────────────────────────────────── */
.app-pagination__controls {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border: 1px solid #e5e7eb; /* gray-200 */
  border-radius: 0.5rem; /* rounded-lg */
  padding: 2px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.app-pagination__pages {
  display: flex;
  align-items: center;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
.app-pagination__btn,
.app-pagination__page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #374151; /* gray-700 */
  transition: all 0.2s ease;
  user-select: none;
}

.app-pagination__btn {
  padding: 0.5rem;
  border-radius: 0.375rem;
}

.app-pagination__btn:hover:not(:disabled) {
  background-color: #f3f4f6; /* gray-100 */
  color: #111827;
}

.app-pagination__btn:disabled {
  color: #d1d5db; /* gray-300 */
  cursor: not-allowed;
}

.app-pagination__page-btn {
  min-width: 2.25rem;
  height: 2.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  margin: 0 2px;
}

.app-pagination__page-btn:hover {
  background-color: #f3f4f6;
}

.app-pagination__page-btn--active {
  background-color: #166534 !important; /* green-800 */
  color: #ffffff !important;
  font-weight: 600;
}

.app-pagination__ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2.25rem;
  color: #9ca3af; /* gray-400 */
  font-size: 0.875rem;
}

/* ── Sizes ───────────────────────────────────────────────────────────────── */
.app-pagination--sm .app-pagination__page-btn {
  min-width: 1.75rem;
  height: 1.75rem;
  font-size: 0.75rem;
}

.app-pagination--sm .app-pagination__btn {
  padding: 0.25rem;
}

.app-pagination--lg .app-pagination__page-btn {
  min-width: 2.75rem;
  height: 2.75rem;
  font-size: 1rem;
}

.app-pagination--lg .app-pagination__btn {
  padding: 0.75rem;
}
</style>
