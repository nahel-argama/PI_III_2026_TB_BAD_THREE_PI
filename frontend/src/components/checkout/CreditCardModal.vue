<template>
  <Teleport to="body">
    <Transition name="cc-modal">
      <div
        v-if="modelValue"
        class="cc-backdrop"
        role="dialog"
        aria-modal="true"
        aria-labelledby="cc-modal-title"
        @click.self="onBackdropClick"
      >
        <div class="cc-panel">
          <!-- Header -->
          <div class="cc-header">
            <div class="cc-header-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
                <line x1="1" y1="10" x2="23" y2="10" />
              </svg>
            </div>
            <div>
              <h2 id="cc-modal-title" class="cc-title">Dados do Cartão de Crédito</h2>
              <p class="cc-subtitle">Preencha os dados para finalizar o pagamento</p>
            </div>
            <button class="cc-close-btn" aria-label="Fechar" :disabled="disabled" @click="onCancel">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <!-- Form body -->
          <div class="cc-body">
            <!-- Número do cartão -->
            <div class="cc-field">
              <label for="cc-number" class="cc-label">Número do cartão</label>
              <input
                id="cc-number"
                v-model="form.number"
                type="text"
                inputmode="numeric"
                maxlength="19"
                placeholder="0000 0000 0000 0000"
                class="cc-input"
                :class="{ 'cc-input--error': errors.number }"
                :disabled="disabled"
                autocomplete="cc-number"
                @input="onNumberInput"
                @blur="validateField('number')"
              />
              <p v-if="errors.number" class="cc-error">{{ errors.number }}</p>
            </div>

            <!-- Nome do titular -->
            <div class="cc-field">
              <label for="cc-holder" class="cc-label">Nome do titular (como no cartão)</label>
              <input
                id="cc-holder"
                v-model="form.holder_name"
                type="text"
                maxlength="120"
                placeholder="NOME SOBRENOME"
                class="cc-input"
                :class="{ 'cc-input--error': errors.holder_name }"
                :disabled="disabled"
                autocomplete="cc-name"
                @input="form.holder_name = form.holder_name.toUpperCase()"
                @blur="validateField('holder_name')"
              />
              <p v-if="errors.holder_name" class="cc-error">{{ errors.holder_name }}</p>
            </div>

            <!-- Validade + CVV -->
            <div class="cc-row">
              <div class="cc-field">
                <label for="cc-month" class="cc-label">Mês</label>
                <select
                  id="cc-month"
                  v-model.number="form.expiry_month"
                  class="cc-input"
                  :class="{ 'cc-input--error': errors.expiry_month }"
                  :disabled="disabled"
                  autocomplete="cc-exp-month"
                  @change="
                    validateField('expiry_month');
                    validateField('expiry_year');
                  "
                >
                  <option :value="null" disabled>MM</option>
                  <option v-for="m in 12" :key="m" :value="m">
                    {{ String(m).padStart(2, '0') }}
                  </option>
                </select>
                <p v-if="errors.expiry_month" class="cc-error">{{ errors.expiry_month }}</p>
              </div>

              <div class="cc-field">
                <label for="cc-year" class="cc-label">Ano</label>
                <select
                  id="cc-year"
                  v-model.number="form.expiry_year"
                  class="cc-input"
                  :class="{ 'cc-input--error': errors.expiry_year }"
                  :disabled="disabled"
                  autocomplete="cc-exp-year"
                  @change="validateField('expiry_year')"
                >
                  <option :value="null" disabled>AAAA</option>
                  <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
                </select>
                <p v-if="errors.expiry_year" class="cc-error">{{ errors.expiry_year }}</p>
              </div>

              <div class="cc-field">
                <label for="cc-cvv" class="cc-label">CVV</label>
                <input
                  id="cc-cvv"
                  v-model="form.cvv"
                  type="text"
                  inputmode="numeric"
                  maxlength="4"
                  placeholder="•••"
                  class="cc-input"
                  :class="{ 'cc-input--error': errors.cvv }"
                  :disabled="disabled"
                  autocomplete="cc-csc"
                  @input="form.cvv = form.cvv.replace(/\D/g, '')"
                  @blur="validateField('cvv')"
                />
                <p v-if="errors.cvv" class="cc-error">{{ errors.cvv }}</p>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="cc-actions">
            <button
              type="button"
              class="cc-btn cc-btn--cancel"
              :disabled="disabled"
              @click="onCancel"
            >
              Cancelar
            </button>
            <button
              type="button"
              class="cc-btn cc-btn--confirm"
              :disabled="!isValid || disabled"
              @click="onConfirm"
            >
              <span v-if="disabled" class="cc-spinner" aria-hidden="true" />
              <span>{{ disabled ? 'Processando…' : 'Continuar' }}</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { reactive, computed } from 'vue';

const props = defineProps({
  /** Controla a visibilidade — use com v-model */
  modelValue: {
    type: Boolean,
    default: false,
  },
  /** Desabilita o formulário e botões (ex: enquanto processa o pagamento) */
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel']);

// ─── Estado do formulário ─────────────────────────────────────────────────────

const currentYear = new Date().getFullYear();
const yearOptions = Array.from({ length: 21 }, (_, i) => currentYear + i);

const form = reactive({
  number: '',
  holder_name: '',
  expiry_month: null,
  expiry_year: null,
  cvv: '',
});

const errors = reactive({
  number: '',
  holder_name: '',
  expiry_month: '',
  expiry_year: '',
  cvv: '',
});

// ─── Máscara ──────────────────────────────────────────────────────────────────

function onNumberInput() {
  const digits = form.number.replace(/\D/g, '').slice(0, 16);
  form.number = digits.replace(/(.{4})/g, '$1 ').trim();
}

// ─── Validação ────────────────────────────────────────────────────────────────

function getFieldError(field) {
  switch (field) {
    case 'number': {
      const digits = form.number.replace(/\s/g, '');
      if (!digits) return 'Número do cartão é obrigatório.';
      if (digits.length < 13 || digits.length > 16) return 'Deve ter entre 13 e 16 dígitos.';
      return '';
    }
    case 'holder_name': {
      const name = form.holder_name.trim();
      if (!name) return 'Nome do titular é obrigatório.';
      if (!/^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$/.test(name)) return 'Apenas letras são permitidas.';
      if (name.split(/\s+/).filter(Boolean).length < 2) return 'Informe nome e sobrenome.';
      return '';
    }
    case 'expiry_month': {
      if (!form.expiry_month) return 'Mês é obrigatório.';
      return '';
    }
    case 'expiry_year': {
      if (!form.expiry_year) return 'Ano é obrigatório.';
      if (form.expiry_month && form.expiry_year) {
        const expiry = new Date(form.expiry_year, form.expiry_month - 1, 1);
        const firstOfNow = new Date(new Date().getFullYear(), new Date().getMonth(), 1);
        if (expiry < firstOfNow) return 'Cartão expirado.';
      }
      return '';
    }
    case 'cvv': {
      if (!form.cvv) return 'CVV é obrigatório.';
      if (!/^\d{3,4}$/.test(form.cvv)) return 'CVV deve ter 3 ou 4 dígitos.';
      return '';
    }
    default:
      return '';
  }
}

function validateField(field) {
  errors[field] = getFieldError(field);
}

function validateAll() {
  ['number', 'holder_name', 'expiry_month', 'expiry_year', 'cvv'].forEach((f) => {
    errors[f] = getFieldError(f);
  });
}

const isValid = computed(() => {
  const hasValues =
    form.number && form.holder_name && form.expiry_month && form.expiry_year && form.cvv;
  if (!hasValues) return false;
  return ['number', 'holder_name', 'expiry_month', 'expiry_year', 'cvv'].every(
    (f) => getFieldError(f) === '',
  );
});

// ─── Ações ────────────────────────────────────────────────────────────────────

function onConfirm() {
  validateAll();
  if (!isValid.value) return;

  emit('confirm', {
    holder_name: form.holder_name.trim(),
    number: form.number.replace(/\s/g, ''),
    expiry_month: form.expiry_month,
    expiry_year: form.expiry_year,
    cvv: form.cvv,
  });
}

function onCancel() {
  if (props.disabled) return;
  emit('cancel');
  emit('update:modelValue', false);
}

function onBackdropClick() {
  if (!props.disabled) onCancel();
}


</script>

<style scoped>
/* ── Backdrop ────────────────────────────────────────────────────────────── */
.cc-backdrop {
  position: fixed;
  inset: 0;
  z-index: 60;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: rgb(2 6 23 / 0.6);
  backdrop-filter: blur(6px);
}

/* ── Panel ───────────────────────────────────────────────────────────────── */
.cc-panel {
  width: 100%;
  max-width: 28rem;
  background: #fff;
  border-radius: 24px;
  box-shadow:
    0 24px 80px rgba(15, 23, 42, 0.24),
    0 0 0 1px rgba(15, 23, 42, 0.04);
  display: flex;
  flex-direction: column;
  gap: 0;
  overflow: hidden;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.cc-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.cc-header-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 12px;
  background: #ecfdf5;
  color: #059669;
}

.cc-header-icon svg {
  width: 1.25rem;
  height: 1.25rem;
}

.cc-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.3;
}

.cc-subtitle {
  margin: 2px 0 0;
  font-size: 0.75rem;
  color: #64748b;
}

.cc-close-btn {
  margin-left: auto;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  transition:
    background 0.15s,
    color 0.15s;
}

.cc-close-btn:hover:not(:disabled) {
  background: #f1f5f9;
  color: #475569;
}

.cc-close-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.cc-close-btn svg {
  width: 1rem;
  height: 1rem;
}

/* ── Body ────────────────────────────────────────────────────────────────── */
.cc-body {
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cc-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.75rem;
}

.cc-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cc-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #475569;
  letter-spacing: 0.02em;
}

.cc-input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #0f172a;
  background: #fff;
  transition:
    border-color 0.15s,
    box-shadow 0.15s;
  outline: none;
  appearance: none;
  box-sizing: border-box;
}

.cc-input:focus {
  border-color: #059669;
  box-shadow: 0 0 0 3px rgb(5 150 105 / 0.12);
}

.cc-input:disabled {
  background: #f8fafc;
  color: #94a3b8;
  cursor: not-allowed;
}

.cc-input--error {
  border-color: #ef4444;
}

.cc-input--error:focus {
  box-shadow: 0 0 0 3px rgb(239 68 68 / 0.12);
}

.cc-error {
  margin: 0;
  font-size: 0.68rem;
  font-weight: 600;
  color: #ef4444;
}

/* ── Actions ─────────────────────────────────────────────────────────────── */
.cc-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem 1.5rem;
  border-top: 1px solid #f1f5f9;
}

.cc-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.7rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition:
    background 0.15s,
    box-shadow 0.15s,
    opacity 0.15s,
    transform 0.1s;
  line-height: 1.2;
}

.cc-btn:active:not(:disabled) {
  transform: scale(0.97);
}

.cc-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.cc-btn--cancel {
  background: #f8fafc;
  color: #475569;
  border: 1.5px solid #e2e8f0;
}

.cc-btn--cancel:hover:not(:disabled) {
  background: #f1f5f9;
}

.cc-btn--confirm {
  background: #059669;
  color: #fff;
  box-shadow: 0 4px 14px rgb(5 150 105 / 0.3);
}

.cc-btn--confirm:hover:not(:disabled) {
  background: #047857;
  box-shadow: 0 6px 18px rgb(5 150 105 / 0.38);
}

/* ── Spinner ─────────────────────────────────────────────────────────────── */
.cc-spinner {
  display: inline-block;
  width: 0.875rem;
  height: 0.875rem;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: cc-spin 0.65s linear infinite;
  flex-shrink: 0;
}

@keyframes cc-spin {
  to {
    transform: rotate(360deg);
  }
}

/* ── Transition ──────────────────────────────────────────────────────────── */
.cc-modal-enter-active {
  transition: opacity 0.2s ease;
}
.cc-modal-enter-active .cc-panel {
  transition:
    opacity 0.2s ease,
    transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.cc-modal-leave-active {
  transition: opacity 0.18s ease;
}
.cc-modal-leave-active .cc-panel {
  transition:
    opacity 0.15s ease,
    transform 0.15s ease;
}

.cc-modal-enter-from {
  opacity: 0;
}
.cc-modal-enter-from .cc-panel {
  opacity: 0;
  transform: scale(0.9) translateY(10px);
}

.cc-modal-leave-to {
  opacity: 0;
}
.cc-modal-leave-to .cc-panel {
  opacity: 0;
  transform: scale(0.96);
}
</style>
