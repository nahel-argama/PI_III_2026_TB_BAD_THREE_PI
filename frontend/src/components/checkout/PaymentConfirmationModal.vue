<template>
  <Teleport to="body">
    <Transition name="pm-modal">
      <div
        v-if="modelValue"
        class="pm-backdrop"
        role="dialog"
        aria-modal="true"
        aria-labelledby="pm-modal-title"
        @click.self="onBackdropClick"
        @keydown.esc="onEsc"
      >
        <div class="pm-panel" :class="[`pm-panel--${size}`]">

          <!-- ═══════════════ IDLE ═══════════════ -->
          <template v-if="currentState === 'idle'">
            <div class="pm-header">
              <div class="pm-header-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" aria-hidden="true">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
              </div>
              <div>
                <h2 id="pm-modal-title" class="pm-title">{{ title }}</h2>
                <p class="pm-subtitle">{{ description }}</p>
              </div>
            </div>

            <div class="pm-body">
              <div class="pm-info-card">
                <div class="pm-info-row pm-info-row--highlight">
                  <span class="pm-info-label">VALOR TOTAL</span>
                  <span class="pm-info-value pm-info-value--big">{{ amount }}</span>
                </div>
                <div class="pm-info-row">
                  <span class="pm-info-label">MÉTODO</span>
                  <span class="pm-info-value">{{ paymentMethod }}</span>
                </div>
              </div>
            </div>

            <div class="pm-actions">
              <button type="button" class="pm-btn pm-btn--cancel" @click="onClose">
                {{ props.cancelLabel || 'Cancelar' }}
              </button>
              <button type="button" class="pm-btn pm-btn--confirm" @click="onConfirm">
                Confirmar pagamento
              </button>
            </div>
          </template>

          <!-- ═══════════════ LOADING ═══════════════ -->
          <template v-else-if="currentState === 'loading'">
            <div class="pm-state-container">
              <div class="pm-pulse-ring" aria-hidden="true">
                <div class="pm-pulse-ring__outer" />
                <div class="pm-pulse-ring__middle" />
                <div class="pm-pulse-ring__inner">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                </div>
              </div>
              <p class="pm-state-title">Processando pagamento</p>
              <p class="pm-state-sub">Aguarde enquanto confirmamos sua transação…</p>
            </div>
          </template>

          <!-- ═══════════════ SUCCESS ═══════════════ -->
          <template v-else-if="currentState === 'success'">
            <div class="pm-state-container">
              <div class="pm-anim-check" aria-hidden="true">
                <svg class="pm-anim-check__svg" viewBox="0 0 52 52">
                  <circle class="pm-anim-check__circle" cx="26" cy="26" r="24"
                    fill="none" stroke-width="2.5"/>
                  <polyline class="pm-anim-check__tick" points="14,27 22,35 38,19"
                    fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <p class="pm-state-title pm-state-title--success">{{ successTitle }}</p>
              <p class="pm-state-sub">{{ successMessage }}</p>
              <button type="button" class="pm-btn pm-btn--success pm-btn--full" @click="onSuccessClose">
                Fechar
              </button>
            </div>
          </template>

          <!-- ═══════════════ ERROR ═══════════════ -->
          <template v-else-if="currentState === 'error'">
            <div class="pm-state-container">
              <div class="pm-anim-error" aria-hidden="true">
                <svg class="pm-anim-error__svg" viewBox="0 0 52 52">
                  <circle class="pm-anim-error__circle" cx="26" cy="26" r="24"
                    fill="none" stroke-width="2.5"/>
                  <line class="pm-anim-error__x1" x1="17" y1="17" x2="35" y2="35"
                    stroke-width="3" stroke-linecap="round"/>
                  <line class="pm-anim-error__x2" x1="35" y1="17" x2="17" y2="35"
                    stroke-width="3" stroke-linecap="round"/>
                </svg>
              </div>
              <p class="pm-state-title pm-state-title--error">{{ errorTitle }}</p>
              <p class="pm-state-sub">{{ errorMessage }}</p>
              <div class="pm-actions pm-actions--stacked">
                <button type="button" class="pm-btn pm-btn--cancel pm-btn--full" @click="onErrorClose">
                  Fechar
                </button>
              </div>
            </div>
          </template>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';

const props = defineProps({
  modelValue:       { type: Boolean, default: false },
  amount:           { type: String, required: true },
  paymentMethod:    { type: String, required: true },

  title:            { type: String, default: 'Confirmar pagamento' },
  description:      { type: String, default: 'Revise os dados antes de prosseguir.' },

  successTitle:     { type: String, default: 'Pagamento realizado!' },
  successMessage:   { type: String, default: 'Sua transação foi processada com sucesso.' },

  errorTitle:       { type: String, default: 'Falha no pagamento' },
  errorMessage:     { type: String, default: 'Ocorreu um erro ao processar seu pagamento.' },

  cancelLabel:      { type: String, default: 'Cancelar' },

  autoClose:        { type: Boolean, default: false },
  autoCloseDelay:   { type: Number, default: 2500 },

  closable:         { type: Boolean, default: true },
  persistent:       { type: Boolean, default: false },

  size:             { type: String, default: 'md' },
});

const emit = defineEmits([
  'update:modelValue',
  'confirm',
  'success',
  'error',
  'retry',
  'close',
]);

// ─── State machine ────────────────────────────────────────────────────────────
const currentState = ref('idle'); // 'idle' | 'loading' | 'success' | 'error'

let autoCloseTimer = null;

function clearTimers() {
  if (autoCloseTimer) { clearTimeout(autoCloseTimer); autoCloseTimer = null; }
}

// ─── Exposed: let parent drive state transitions ──────────────────────────────
function setState(s) {
  currentState.value = s;
  if (s === 'success') {
    emit('success');
    if (props.autoClose) {
      autoCloseTimer = setTimeout(() => onSuccessClose(), props.autoCloseDelay);
    }
  }
  if (s === 'error') { emit('error'); }
}

defineExpose({ setState, state: currentState });

// ─── Actions ──────────────────────────────────────────────────────────────────
function close() {
  clearTimers();
  emit('update:modelValue', false);
  emit('close');
}

function onClose() {
  if (!props.closable || props.persistent) return;
  close();
}

function onBackdropClick() {
  if (currentState.value === 'loading' || props.persistent) return;
  onClose();
}

function onEsc() {
  if (currentState.value === 'loading') return;
  onClose();
}

function onConfirm() {
  if (currentState.value !== 'idle') return;
  currentState.value = 'loading';
  emit('confirm');
}

function onRetry() {
  emit('retry');
}

function onSuccessClose() {
  clearTimers();
  emit('success');
  close();
}

function onErrorClose() {
  close();
}

// Reset state when modal opens
watch(() => props.modelValue, (opened) => {
  if (opened) {
    currentState.value = 'idle';
    clearTimers();
  }
});

onBeforeUnmount(() => clearTimers());
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════════════════════
   Design tokens (matching CreditCardModal exactly)
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── Backdrop ────────────────────────────────────────────────────────────── */
.pm-backdrop {
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
.pm-panel {
  width: 100%;
  background: #fff;
  border-radius: 24px;
  box-shadow:
    0 24px 80px rgba(15, 23, 42, 0.24),
    0 0 0 1px rgba(15, 23, 42, 0.04);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pm-panel--sm { max-width: 22rem; }
.pm-panel--md { max-width: 28rem; }
.pm-panel--lg { max-width: 34rem; }

/* ── Header (same structure as CreditCardModal) ──────────────────────────── */
.pm-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.pm-header-icon {
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

.pm-header-icon svg {
  width: 1.25rem;
  height: 1.25rem;
}

.pm-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.3;
}

.pm-subtitle {
  margin: 2px 0 0;
  font-size: 0.75rem;
  color: #64748b;
}

/* ── Body ────────────────────────────────────────────────────────────────── */
.pm-body {
  padding: 1.25rem 1.5rem;
}

.pm-info-card {
  border: 2px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden;
}

.pm-info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 1rem;
}

.pm-info-row--highlight {
  background: #f8fafc;
  border-bottom: 1.5px solid #e2e8f0;
}

.pm-info-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.06em;
}

.pm-info-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

.pm-info-value--big {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
}

/* ── Actions (same as CreditCardModal) ───────────────────────────────────── */
.pm-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem 1.5rem;
  border-top: 1px solid #f1f5f9;
}

.pm-actions--stacked {
  grid-template-columns: 1fr;
  padding-top: 0.5rem;
}

/* ── Buttons (same tokens as CreditCardModal) ────────────────────────────── */
.pm-btn {
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
  transition: background 0.15s, box-shadow 0.15s, opacity 0.15s, transform 0.1s;
  line-height: 1.2;
}

.pm-btn:active:not(:disabled) { transform: scale(0.97); }
.pm-btn:disabled { opacity: 0.45; cursor: not-allowed; }
.pm-btn--full { width: 100%; }

.pm-btn--cancel {
  background: #f8fafc;
  color: #475569;
  border: 1.5px solid #e2e8f0;
}
.pm-btn--cancel:hover:not(:disabled) { background: #f1f5f9; }

.pm-btn--confirm {
  background: #059669;
  color: #fff;
  box-shadow: 0 4px 14px rgb(5 150 105 / 0.3);
}
.pm-btn--confirm:hover:not(:disabled) {
  background: #047857;
  box-shadow: 0 6px 18px rgb(5 150 105 / 0.38);
}

.pm-btn--success {
  background: #059669;
  color: #fff;
  box-shadow: 0 4px 14px rgb(5 150 105 / 0.28);
  margin-top: 0.5rem;
}
.pm-btn--success:hover:not(:disabled) { background: #047857; }

/* ═══════════════════════════════════════════════════════════════════════════
   STATES — Loading / Success / Error
   ═══════════════════════════════════════════════════════════════════════ */

.pm-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2.5rem 1.5rem 2rem;
  gap: 0.5rem;
}

.pm-state-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
}
.pm-state-title--success { color: #059669; }
.pm-state-title--error   { color: #dc2626; }

.pm-state-sub {
  margin: 0 0 0.25rem;
  font-size: 0.8rem;
  color: #64748b;
  line-height: 1.55;
  max-width: 20rem;
}

/* ── Loading: pulse ring ─────────────────────────────────────────────────── */
.pm-pulse-ring {
  position: relative;
  width: 5rem;
  height: 5rem;
  margin-bottom: 0.75rem;
}

.pm-pulse-ring__outer,
.pm-pulse-ring__middle {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: #059669;
  animation: pm-spin linear infinite;
}

.pm-pulse-ring__outer  { animation-duration: 1s; }
.pm-pulse-ring__middle {
  inset: 10px;
  border-top-color: rgba(5, 150, 105, 0.4);
  animation-duration: 0.75s;
  animation-direction: reverse;
}

.pm-pulse-ring__inner {
  position: absolute;
  inset: 20px;
  border-radius: 50%;
  background: #ecfdf5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #059669;
  animation: pm-pulse 1.6s ease-in-out infinite;
}

.pm-pulse-ring__inner svg {
  width: 1rem;
  height: 1rem;
}

@keyframes pm-spin {
  to { transform: rotate(360deg); }
}

@keyframes pm-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%      { transform: scale(0.92); opacity: 0.7; }
}

/* ── Loading: progress bar ───────────────────────────────────────────────── */
.pm-progress-track {
  width: 80%;
  height: 4px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.75rem;
}

.pm-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #059669, #34d399);
  border-radius: 4px;
  animation: pm-progress 2s ease-in-out infinite;
}

@keyframes pm-progress {
  0%   { width: 0%; }
  50%  { width: 70%; }
  100% { width: 100%; }
}

/* ── Success: animated check ─────────────────────────────────────────────── */
.pm-anim-check {
  width: 4.5rem;
  height: 4.5rem;
  margin-bottom: 0.5rem;
}

.pm-anim-check__svg {
  width: 100%;
  height: 100%;
}

.pm-anim-check__circle {
  stroke: #059669;
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  animation: pm-draw-circle 0.5s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.pm-anim-check__tick {
  stroke: #059669;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: pm-draw-tick 0.3s ease forwards 0.4s;
}

@keyframes pm-draw-circle {
  to { stroke-dashoffset: 0; }
}

@keyframes pm-draw-tick {
  to { stroke-dashoffset: 0; }
}

/* ── Error: animated X ───────────────────────────────────────────────────── */
.pm-anim-error {
  width: 4.5rem;
  height: 4.5rem;
  margin-bottom: 0.5rem;
}

.pm-anim-error__svg {
  width: 100%;
  height: 100%;
}

.pm-anim-error__circle {
  stroke: #dc2626;
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  animation: pm-draw-circle 0.5s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.pm-anim-error__x1,
.pm-anim-error__x2 {
  stroke: #dc2626;
  stroke-dasharray: 28;
  stroke-dashoffset: 28;
}

.pm-anim-error__x1 { animation: pm-draw-tick 0.25s ease forwards 0.4s; }
.pm-anim-error__x2 { animation: pm-draw-tick 0.25s ease forwards 0.55s; }

/* ═══════════════════════════════════════════════════════════════════════════
   MODAL TRANSITION (matching CreditCardModal)
   ═══════════════════════════════════════════════════════════════════════ */
.pm-modal-enter-active {
  transition: opacity 0.2s ease;
}
.pm-modal-enter-active .pm-panel {
  transition: opacity 0.2s ease, transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.pm-modal-leave-active {
  transition: opacity 0.18s ease;
}
.pm-modal-leave-active .pm-panel {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.pm-modal-enter-from { opacity: 0; }
.pm-modal-enter-from .pm-panel { opacity: 0; transform: scale(0.9) translateY(10px); }

.pm-modal-leave-to { opacity: 0; }
.pm-modal-leave-to .pm-panel { opacity: 0; transform: scale(0.96); }
</style>
