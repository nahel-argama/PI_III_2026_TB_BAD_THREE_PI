<template>
  <div
    class="app-select"
    :class="[$attrs.class, { 'app-select--open': isOpen, 'app-select--disabled': disabled }]"
  >
    <!-- Label -->
    <label v-if="label" :for="inputId" class="app-select__label">
      {{ label }}
      <span v-if="required" class="app-select__required" aria-hidden="true">*</span>
    </label>

    <!-- Trigger / Autocomplete input wrapper -->
    <div
      ref="triggerRef"
      class="app-select__trigger"
      :class="{
        'app-select__trigger--focused': isOpen,
        'app-select__trigger--error': !!error,
        'app-select__trigger--sm': size === 'sm',
        'app-select__trigger--lg': size === 'lg',
      }"
      @click="!autocomplete && toggleDropdown()"
    >
      <!-- Leading icon slot -->
      <span v-if="$slots['icon-left']" class="app-select__icon-left">
        <slot name="icon-left" />
      </span>

      <!-- Autocomplete input -->
      <template v-if="autocomplete">
        <!--
          Hidden input: holds the real modelValue so that native browser
          form validation (required) works correctly even when `query` is empty
          after the user selects an option and the search field is cleared.
        -->
        <input
          type="text"
          aria-hidden="true"
          tabindex="-1"
          :value="modelValue ?? ''"
          :required="required"
          style="position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none"
        />

        <input
          :id="inputId"
          ref="inputRef"
          v-model="query"
          type="text"
          :class="['app-select__input', { 'app-select__input--has-selection': !!selectedLabel }]"
          :placeholder="selectedLabel || placeholder"
          :disabled="disabled"
          autocomplete="off"
          role="combobox"
          :aria-expanded="shouldShowDropdown"
          :aria-controls="listboxId"
          :aria-activedescendant="activeDescendant"
          @focus="openDropdown"
          @keydown="handleKeydown"
          @input="onInput"
        />
      </template>

      <!-- Read-only display (non-autocomplete) -->
      <span
        v-else
        :id="inputId"
        class="app-select__display"
        :class="{ 'app-select__display--placeholder': !selectedLabel }"
        tabindex="0"
        role="combobox"
        :aria-expanded="shouldShowDropdown"
        :aria-controls="listboxId"
        :aria-activedescendant="activeDescendant"
        @keydown="handleKeydown"
      >
        {{ selectedLabel || placeholder }}
      </span>

      <!-- Clear button -->
      <button
        v-if="clearable && modelValue !== null && modelValue !== undefined && modelValue !== ''"
        type="button"
        class="app-select__clear"
        aria-label="Limpar seleção"
        @click.stop="clear"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14" aria-hidden="true">
          <path
            d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z"
          />
        </svg>
      </button>

      <!-- Chevron -->
      <span
        class="app-select__chevron"
        :class="{ 'app-select__chevron--open': isOpen }"
        aria-hidden="true"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
          <path
            fill-rule="evenodd"
            d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z"
            clip-rule="evenodd"
          />
        </svg>
      </span>
    </div>

    <!-- Hint / Error -->
    <p v-if="error" class="app-select__error" role="alert">{{ error }}</p>
    <p v-else-if="hint" class="app-select__hint">{{ hint }}</p>

    <!-- Dropdown -->
    <Teleport to="body">
      <Transition name="app-select-dropdown">
        <div
          v-if="shouldShowDropdown"
          :id="listboxId"
          ref="dropdownRef"
          class="app-select__dropdown"
          :style="dropdownStyle"
          role="listbox"
          :aria-label="label || placeholder"
          @mousedown.prevent
        >
          <!-- Loading state -->
          <div v-if="loading" class="app-select__state">
            <span class="app-select__spinner" aria-hidden="true" />
            <span>{{ loadingText }}</span>
          </div>

          <!-- Empty state -->
          <div
            v-else-if="filteredOptions.length === 0"
            class="app-select__state app-select__state--empty"
          >
            <slot name="empty">{{ emptyText }}</slot>
          </div>

          <!-- Options list -->
          <template v-else>
            <div
              v-for="(option, index) in filteredOptions"
              :id="`${listboxId}-option-${index}`"
              :key="optionKey(option)"
              role="option"
              :aria-selected="isSelected(option)"
              class="app-select__option"
              :class="{
                'app-select__option--selected': isSelected(option),
                'app-select__option--active': activeIndex === index,
                'app-select__option--disabled': option.disabled,
              }"
              @click="!option.disabled && selectOption(option)"
              @mouseenter="activeIndex = index"
            >
              <!-- Option leading slot -->
              <slot name="option" :option="option" :selected="isSelected(option)">
                <span class="app-select__option-label">{{ optionLabel(option) }}</span>
                <!-- Checkmark for selected -->
                <span v-if="isSelected(option)" class="app-select__option-check" aria-hidden="true">
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                    <path
                      fill-rule="evenodd"
                      d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </span>
              </slot>
            </div>
          </template>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';

// ─── Props ────────────────────────────────────────────────────────────────────

const props = defineProps({
  /** Valor selecionado (v-model) */
  modelValue: {
    default: null,
  },

  /** Lista de opções. Pode ser array de primitivos ou de objetos { label, value, disabled? } */
  options: {
    type: Array,
    default: () => [],
  },

  /** Habilita modo autocomplete (filtra opções conforme o usuário digita) */
  autocomplete: {
    type: Boolean,
    default: false,
  },

  /** Delay do debounce para o evento @search (ms) */
  debounceDelay: {
    type: Number,
    default: 300,
  },

  /** Chave do objeto usada como valor. Para arrays de primitivos, deixar null. */
  valueKey: {
    type: String,
    default: 'value',
  },

  /** Chave do objeto usada como label. Para arrays de primitivos, deixar null. */
  labelKey: {
    type: String,
    default: 'label',
  },

  /** Texto exibido quando nenhuma opção está selecionada */
  placeholder: {
    type: String,
    default: 'Selecione uma opção',
  },

  /** Label acima do campo */
  label: {
    type: String,
    default: '',
  },

  /** Texto de dica abaixo do campo */
  hint: {
    type: String,
    default: '',
  },

  /** Mensagem de erro (substitui hint) */
  error: {
    type: String,
    default: '',
  },

  /** Tamanho: 'sm' | 'md' | 'lg' */
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },

  /** Desabilita o componente */
  disabled: {
    type: Boolean,
    default: false,
  },

  /** Campo obrigatório */
  required: {
    type: Boolean,
    default: false,
  },

  /** Exibe botão de limpar seleção */
  clearable: {
    type: Boolean,
    default: false,
  },

  /** Texto quando não há opções */
  emptyText: {
    type: String,
    default: 'Nenhuma opção encontrada',
  },

  /** Exibe estado de carregamento na lista */
  loading: {
    type: Boolean,
    default: false,
  },

  /** Texto exibido durante carregamento */
  loadingText: {
    type: String,
    default: 'Carregando…',
  },

  /**
   * Filtragem interna de opções no modo autocomplete.
   * Defina como false se a filtragem for feita externamente via @search.
   */
  filterLocally: {
    type: Boolean,
    default: true,
  },
});

// ─── Emits ───────────────────────────────────────────────────────────────────

const emit = defineEmits([
  /** Novo valor selecionado */
  'update:modelValue',
  /** Opção selecionada completa */
  'select',
  /** Seleção limpa */
  'clear',
  /** Disparado com debounce quando o usuário digita (autocomplete) */
  'search',
  /** Dropdown aberto */
  'open',
  /** Dropdown fechado */
  'close',
]);

// ─── Refs & state ────────────────────────────────────────────────────────────

const isOpen = ref(false);
const query = ref('');
const activeIndex = ref(-1);
const triggerRef = ref(null);
const inputRef = ref(null);
const dropdownRef = ref(null);
const dropdownStyle = ref({});

// IDs únicos (acessibilidade)
const uid = Math.random().toString(36).slice(2, 9);
const inputId = `app-select-input-${uid}`;
const listboxId = `app-select-listbox-${uid}`;

// Debounce timer
let debounceTimer = null;

// ─── Computed ────────────────────────────────────────────────────────────────

/**
 * Retorna o label de uma opção (primitivo ou objeto).
 */
function optionLabel(option) {
  if (option === null || option === undefined) return '';
  if (typeof option === 'object') return option[props.labelKey] ?? String(option);
  return String(option);
}

/**
 * Retorna o value de uma opção (primitivo ou objeto).
 */
function optionValue(option) {
  if (option === null || option === undefined) return option;
  if (typeof option === 'object') return option[props.valueKey] ?? option;
  return option;
}

/**
 * Chave única para v-for.
 */
function optionKey(option) {
  return String(optionValue(option));
}

/**
 * Label da opção atualmente selecionada.
 */
const selectedLabel = computed(() => {
  if (props.modelValue === null || props.modelValue === undefined || props.modelValue === '')
    return '';
  const found = props.options.find((o) => String(optionValue(o)) === String(props.modelValue));
  return found ? optionLabel(found) : String(props.modelValue);
});

/**
 * Opções filtradas (autocomplete local ou lista completa).
 */
const filteredOptions = computed(() => {
  if (!props.autocomplete || !props.filterLocally || !query.value.trim()) {
    return props.options;
  }
  const q = query.value.trim().toLowerCase();
  return props.options.filter((o) => optionLabel(o).toLowerCase().includes(q));
});

/**
 * aria-activedescendant
 */
const activeDescendant = computed(() =>
  activeIndex.value >= 0 ? `${listboxId}-option-${activeIndex.value}` : undefined,
);

const shouldShowDropdown = computed(() => {
  if (!isOpen.value) return false;
  if (
    props.autocomplete &&
    !query.value.trim() &&
    !props.loading &&
    filteredOptions.value.length === 0
  ) {
    return false;
  }
  return true;
});

// ─── Methods ─────────────────────────────────────────────────────────────────

function isSelected(option) {
  return String(optionValue(option)) === String(props.modelValue);
}

function openDropdown() {
  if (props.disabled || isOpen.value) return;
  isOpen.value = true;
  activeIndex.value = props.options.findIndex((o) => isSelected(o));
  positionDropdown();
  emit('open');
}

function closeDropdown() {
  if (!isOpen.value) return;
  isOpen.value = false;
  activeIndex.value = -1;

  if (props.autocomplete) {
    // Restaura o query para o label selecionado (ou limpa se nada selecionado)
    query.value = '';
  }

  emit('close');
}

function toggleDropdown() {
  if (props.disabled) return;
  if (isOpen.value) {
    closeDropdown();
  } else {
    openDropdown();
  }
}

function selectOption(option) {
  const value = optionValue(option);
  emit('update:modelValue', value);
  emit('select', option);
  closeDropdown();

  if (props.autocomplete && inputRef.value) {
    nextTick(() => inputRef.value?.blur());
  }
}

function clear() {
  emit('update:modelValue', null);
  emit('clear');
  query.value = '';
}

// ─── Autocomplete / debounce ─────────────────────────────────────────────────

function onInput() {
  if (!isOpen.value) openDropdown();
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    emit('search', query.value);
  }, props.debounceDelay);
}

// ─── Keyboard navigation ─────────────────────────────────────────────────────

function handleKeydown(e) {
  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault();
      if (!isOpen.value) {
        openDropdown();
      } else {
        activeIndex.value = Math.min(activeIndex.value + 1, filteredOptions.value.length - 1);
        scrollActiveIntoView();
      }
      break;
    case 'ArrowUp':
      e.preventDefault();
      activeIndex.value = Math.max(activeIndex.value - 1, 0);
      scrollActiveIntoView();
      break;
    case 'Enter':
      e.preventDefault();
      if (isOpen.value && activeIndex.value >= 0) {
        const option = filteredOptions.value[activeIndex.value];
        if (option && !option.disabled) selectOption(option);
      } else {
        openDropdown();
      }
      break;
    case 'Escape':
      closeDropdown();
      break;
    case 'Tab':
      closeDropdown();
      break;
  }
}

function scrollActiveIntoView() {
  nextTick(() => {
    const el = dropdownRef.value?.querySelector(`#${listboxId}-option-${activeIndex.value}`);
    el?.scrollIntoView({ block: 'nearest' });
  });
}

// ─── Dropdown positioning ────────────────────────────────────────────────────

function positionDropdown() {
  nextTick(() => {
    if (!triggerRef.value) return;
    const rect = triggerRef.value.getBoundingClientRect();
    const viewportHeight = window.innerHeight;
    const spaceBelow = viewportHeight - rect.bottom;
    const spaceAbove = rect.top;
    const maxDropdownHeight = 260;

    const showAbove = spaceBelow < maxDropdownHeight && spaceAbove > spaceBelow;

    dropdownStyle.value = {
      position: 'fixed',
      left: `${rect.left}px`,
      width: `${rect.width}px`,
      zIndex: 9999,
      ...(showAbove
        ? { bottom: `${viewportHeight - rect.top + 6}px`, top: 'auto' }
        : { top: `${rect.bottom + 6}px`, bottom: 'auto' }),
    };
  });
}

// ─── Click outside ───────────────────────────────────────────────────────────

function onClickOutside(e) {
  if (!triggerRef.value?.contains(e.target) && !dropdownRef.value?.contains(e.target)) {
    closeDropdown();
  }
}

// ─── Lifecycle ───────────────────────────────────────────────────────────────

onMounted(() => {
  document.addEventListener('mousedown', onClickOutside);
  window.addEventListener('resize', positionDropdown);
  window.addEventListener('scroll', positionDropdown, true);
});

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onClickOutside);
  window.removeEventListener('resize', positionDropdown);
  window.removeEventListener('scroll', positionDropdown, true);
  clearTimeout(debounceTimer);
});

// Sincroniza query quando modelValue muda externamente
watch(
  () => props.modelValue,
  () => {
    if (!isOpen.value && props.autocomplete) {
      query.value = '';
    }
  },
);
</script>

<style scoped>
/* ── Root ──────────────────────────────────────────────────────────────── */
.app-select {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0;
  width: 100%;
}

.app-select--disabled {
  opacity: 0.55;
  pointer-events: none;
}

/* ── Label ─────────────────────────────────────────────────────────────── */
.app-select__label {
  display: block;
  font-size: 0.875rem;
  font-weight: 700;
  color: #374151; /* gray-700 */
  margin-bottom: 0.5rem; /* mb-2 */
}

.app-select__required {
  color: #dc2626; /* red-600 */
  font-size: 0.875rem;
  margin-left: 2px;
}

/* ── Trigger ───────────────────────────────────────────────────────────── */
.app-select__trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  border-radius: 0.5rem; /* rounded-lg */
  border: 1px solid #1f2937; /* gray-800 - even darker border as requested */
  background-color: #ffffff;
  padding: 0 12px;
  height: 40px;
  cursor: pointer;
  transition:
    border-color 0.15s ease,
    box-shadow 0.15s ease;
  user-select: none;
}

.app-select__trigger:hover:not(.app-select--disabled .app-select__trigger) {
  border-color: #111827; /* gray-900 */
}

.app-select__trigger--focused {
  border-color: #166534; /* green-800 */
  box-shadow: 0 0 0 2px #166534; /* ring-2 green-800 */
  outline: none;
}

.app-select__trigger--error {
  border-color: #dc2626;
  box-shadow: 0 0 0 2px #fee2e2;
}

/* Sizes */
.app-select__trigger--sm {
  height: 32px;
  border-radius: 0.375rem;
}

.app-select__trigger--lg {
  height: 48px;
  border-radius: 0.75rem;
}

/* ── Input (autocomplete) ──────────────────────────────────────────────── */
.app-select__input {
  flex: 1;
  min-width: 0;
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.875rem;
  color: #111827; /* gray-900 */
  padding: 0;
}

.app-select__input::placeholder {
  color: #6b7280; /* gray-500 */
}

/* Quando tem uma seleção no autocomplete, o placeholder age como texto selecionado */
.app-select__input--has-selection::placeholder {
  color: #111827; /* gray-900 */
}

/* ── Display (read-only) ───────────────────────────────────────────────── */
.app-select__display {
  flex: 1;
  min-width: 0;
  font-size: 0.875rem;
  color: #111827; /* gray-900 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  outline: none;
}

.app-select__display--placeholder {
  color: #6b7280; /* gray-500 */
}

/* ── Icons ─────────────────────────────────────────────────────────────── */
.app-select__icon-left {
  display: flex;
  align-items: center;
  color: #6b7280;
}

.app-select__clear {
  color: #9ca3af;
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
}

.app-select__chevron {
  color: #9ca3af;
  transition: transform 0.2s ease;
}

.app-select__chevron--open {
  transform: rotate(180deg);
}

/* ── Hint / Error ──────────────────────────────────────────────────────── */
.app-select__hint,
.app-select__error {
  font-size: 0.75rem;
  margin-top: 4px;
}

.app-select__error {
  color: #dc2626;
}

.app-select__hint {
  color: #6b7280;
}

/* ── Dropdown ──────────────────────────────────────────────────────────── */
.app-select__dropdown {
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  overflow: hidden;
  max-height: 260px;
  overflow-y: auto;
  padding: 4px;
  z-index: 9999;
}

/* ── Option ────────────────────────────────────────────────────────────── */
.app-select__option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #111827;
  cursor: pointer;
}

.app-select__option:hover,
.app-select__option--active {
  background-color: #f3f4f6;
}

.app-select__option--selected {
  color: #166534;
  font-weight: 600;
  background-color: #f0fdf4;
}

.app-select__option-check {
  color: #166534;
}

/* ── Empty / Loading state ─────────────────────────────────────────────── */
.app-select__state {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  font-size: 0.875rem;
  color: #6b7280;
}

.app-select__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #f3f4f6;
  border-top-color: #166534;
  border-radius: 9999px;
  animation: app-select-spin 0.6s linear infinite;
}

@keyframes app-select-spin {
  to {
    transform: rotate(360deg);
  }
}

/* ── Dropdown transition ───────────────────────────────────────────────── */
.app-select-dropdown-enter-active,
.app-select-dropdown-leave-active {
  transition:
    opacity 0.15s ease,
    transform 0.15s ease;
}

.app-select-dropdown-enter-from,
.app-select-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
