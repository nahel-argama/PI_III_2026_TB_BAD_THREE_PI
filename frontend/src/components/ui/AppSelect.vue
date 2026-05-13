<template>
  <div class="app-select" :class="[$attrs.class, { 'app-select--open': isOpen, 'app-select--disabled': disabled }]">
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
          style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;"
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
          :aria-expanded="isOpen"
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
        :aria-expanded="isOpen"
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
          <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
        </svg>
      </button>

      <!-- Chevron -->
      <span class="app-select__chevron" :class="{ 'app-select__chevron--open': isOpen }" aria-hidden="true">
        <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
          <path fill-rule="evenodd" d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
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
          v-if="isOpen"
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
          <div v-else-if="filteredOptions.length === 0" class="app-select__state app-select__state--empty">
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
                    <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clip-rule="evenodd" />
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
  if (props.modelValue === null || props.modelValue === undefined || props.modelValue === '') return '';
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
  isOpen.value ? closeDropdown() : openDropdown();
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
  if (
    !triggerRef.value?.contains(e.target) &&
    !dropdownRef.value?.contains(e.target)
  ) {
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
  gap: 6px;
  width: 100%;
}

.app-select--disabled {
  opacity: 0.55;
  pointer-events: none;
}

/* ── Label ─────────────────────────────────────────────────────────────── */
.app-select__label {
  font-size: 0.875rem;
  font-weight: 700;
  color: #0f172a; /* slate-900 */
  display: flex;
  gap: 3px;
  align-items: center;
  margin-left: 4px;
}

.app-select__required {
  color: #dc2626; /* red-600 */
  font-size: 0.875rem;
}

/* ── Trigger ───────────────────────────────────────────────────────────── */
.app-select__trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  border-radius: 1rem; /* rounded-2xl */
  border: 1px solid #e2e8f0; /* slate-200 */
  background-color: #f8fafc; /* slate-50 */
  padding: 0 14px;
  height: 44px; /* md default */
  cursor: pointer;
  transition:
    border-color 0.15s ease,
    background-color 0.15s ease,
    box-shadow 0.15s ease,
    transform 0.1s ease;
  user-select: none;
}

.app-select__trigger:hover:not(.app-select--disabled .app-select__trigger) {
  border-color: #cbd5e1; /* slate-300 */
  background-color: #fff;
}

.app-select__trigger:active:not(.app-select--disabled .app-select__trigger) {
  transform: scale(0.995);
}

.app-select__trigger--focused {
  border-color: #10b981; /* emerald-500 */
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
  outline: none;
}

.app-select__trigger--error {
  border-color: #fca5a5; /* red-300 */
  box-shadow: 0 0 0 4px #fee2e2; /* red-100 */
}

/* Sizes */
.app-select__trigger--sm {
  height: 36px;
  border-radius: 0.75rem;
  padding: 0 12px;
}

.app-select__trigger--lg {
  height: 52px;
  border-radius: 1.25rem;
  padding: 0 18px;
}

/* ── Input (autocomplete) ──────────────────────────────────────────────── */
.app-select__input {
  flex: 1;
  min-width: 0;
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.875rem;
  color: #0f172a; /* slate-900 */
  padding: 0;
  cursor: text;
}

.app-select__input::placeholder {
  color: #94a3b8; /* slate-400 */
  transition: color 0.2s ease;
}

.app-select__input--has-selection::placeholder {
  color: #475569; /* slate-600 */
}

/* ── Display (read-only) ───────────────────────────────────────────────── */
.app-select__display {
  flex: 1;
  min-width: 0;
  font-size: 0.875rem;
  color: #0f172a; /* slate-900 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  outline: none;
}

.app-select__display:focus-visible {
  outline: none;
}

.app-select__display--placeholder {
  color: #94a3b8; /* slate-400 */
}

/* ── Icons ─────────────────────────────────────────────────────────────── */
.app-select__icon-left {
  display: flex;
  align-items: center;
  color: #64748b; /* slate-500 */
  flex-shrink: 0;
}

.app-select__clear {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #94a3b8; /* slate-400 */
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: color 0.1s;
  border-radius: 9999px;
}

.app-select__clear:hover {
  color: #475569; /* slate-600 */
}

.app-select__chevron {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  color: #94a3b8;
  transition: transform 0.2s ease;
}

.app-select__chevron--open {
  transform: rotate(180deg);
}

/* ── Hint / Error ──────────────────────────────────────────────────────── */
.app-select__hint {
  font-size: 0.75rem;
  color: #64748b; /* slate-500 */
  margin: 0;
}

.app-select__error {
  font-size: 0.75rem;
  color: #dc2626; /* red-600 */
  margin: 0;
}

/* ── Dropdown ──────────────────────────────────────────────────────────── */
.app-select__dropdown {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  box-shadow:
    0 10px 40px rgba(15, 23, 42, 0.12),
    0 2px 8px rgba(15, 23, 42, 0.06);
  overflow: hidden;
  max-height: 260px;
  overflow-y: auto;
  padding: 6px;

  /* Scrollbar minimalista */
  scrollbar-width: thin;
  scrollbar-color: #e2e8f0 transparent;
}

.app-select__dropdown::-webkit-scrollbar {
  width: 4px;
}
.app-select__dropdown::-webkit-scrollbar-track {
  background: transparent;
}
.app-select__dropdown::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 9999px;
}

/* ── Option ────────────────────────────────────────────────────────────── */
.app-select__option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  color: #0f172a;
  cursor: pointer;
  transition: background-color 0.1s;
}

.app-select__option:hover,
.app-select__option--active {
  background-color: #f1f5f9; /* slate-100 */
}

.app-select__option--selected {
  color: #059669; /* emerald-600 */
  font-weight: 600;
  background-color: #ecfdf5; /* emerald-50 */
}

.app-select__option--selected:hover,
.app-select__option--selected.app-select__option--active {
  background-color: #d1fae5; /* emerald-100 */
}

.app-select__option--disabled {
  opacity: 0.45;
  cursor: not-allowed;
  pointer-events: none;
}

.app-select__option-label {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.app-select__option-check {
  display: flex;
  align-items: center;
  color: #059669;
  flex-shrink: 0;
}

/* ── Empty / Loading state ─────────────────────────────────────────────── */
.app-select__state {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  font-size: 0.875rem;
  color: #64748b;
}

.app-select__state--empty {
  justify-content: center;
}

.app-select__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #e2e8f0;
  border-top-color: #059669;
  border-radius: 9999px;
  animation: app-select-spin 0.6s linear infinite;
  flex-shrink: 0;
}

@keyframes app-select-spin {
  to { transform: rotate(360deg); }
}

/* ── Dropdown transition ───────────────────────────────────────────────── */
.app-select-dropdown-enter-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.app-select-dropdown-leave-active {
  transition: opacity 0.1s ease, transform 0.1s ease;
}
.app-select-dropdown-enter-from,
.app-select-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
