<template>
  <Teleport to="body">
    <Transition name="app-dialog">
      <div
        v-if="modelValue"
        class="app-dialog-backdrop"
        role="dialog"
        :aria-modal="true"
        :aria-labelledby="dialogTitleId"
        :aria-describedby="message ? dialogDescId : undefined"
        @click.self="onBackdropClick"
      >
        <div class="app-dialog-panel" :class="`app-dialog-panel--${resolvedVariant}`">
          <!-- Icon -->
          <div class="app-dialog-icon-wrap" :class="`app-dialog-icon-wrap--${resolvedVariant}`">
            <component :is="resolvedIcon" class="app-dialog-icon" aria-hidden="true" />
          </div>

          <!-- Header -->
          <div class="app-dialog-header">
            <h2 :id="dialogTitleId" class="app-dialog-title">{{ title }}</h2>
            <p v-if="message" :id="dialogDescId" class="app-dialog-message">{{ message }}</p>
          </div>

          <!-- Extra slot (e.g. form fields, custom content) -->
          <div v-if="$slots.default" class="app-dialog-slot">
            <slot />
          </div>

          <!-- Actions -->
          <div class="app-dialog-actions" :class="{ 'app-dialog-actions--single': !showCancel }">
            <!-- Cancel / secondary -->
            <button
              v-if="showCancel"
              type="button"
              class="app-dialog-btn app-dialog-btn--cancel"
              :disabled="loading"
              @click="onCancel"
            >
              {{ cancelLabel }}
            </button>

            <!-- Confirm / primary -->
            <button
              type="button"
              class="app-dialog-btn"
              :class="`app-dialog-btn--${resolvedVariant}`"
              :disabled="loading"
              @click="onConfirm"
            >
              <span v-if="loading" class="app-dialog-spinner" aria-hidden="true" />
              <span>{{ loading ? loadingLabel : confirmLabel }}</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  TrashIcon,
  QuestionMarkCircleIcon,
  XCircleIcon,
} from '@heroicons/vue/24/outline';

// ── Props ─────────────────────────────────────────────────────────────────────

const props = defineProps({
  /** Controls visibility — use with v-model */
  modelValue: {
    type: Boolean,
    default: false,
  },

  /**
   * Preset variant that drives the color scheme and default icon.
   * 'info' | 'success' | 'warning' | 'danger' | 'confirm' | 'delete'
   */
  variant: {
    type: String,
    default: 'info',
    validator: (v) => ['info', 'success', 'warning', 'danger', 'confirm', 'delete'].includes(v),
  },

  /** Dialog title (required) */
  title: {
    type: String,
    required: true,
  },

  /** Optional subtitle / description message */
  message: {
    type: String,
    default: '',
  },

  /** Custom icon component (Heroicons or any Vue component). Overrides variant default. */
  icon: {
    type: [Object, Function],
    default: null,
  },

  /** Label for the primary action button */
  confirmLabel: {
    type: String,
    default: 'Confirmar',
  },

  /** Label for the secondary/cancel button */
  cancelLabel: {
    type: String,
    default: 'Cancelar',
  },

  /** Label shown on confirm button while loading is true */
  loadingLabel: {
    type: String,
    default: 'Aguarde…',
  },

  /** Whether to show the cancel button. Set false for alert-only dialogs. */
  showCancel: {
    type: Boolean,
    default: true,
  },

  /** Shows a spinner on the confirm button and disables both buttons */
  loading: {
    type: Boolean,
    default: false,
  },

  /** Whether clicking the backdrop closes the dialog (emits cancel) */
  closeOnBackdrop: {
    type: Boolean,
    default: true,
  },

  /** Unique suffix for aria IDs — useful when multiple dialogs coexist */
  dialogId: {
    type: String,
    default: () => `dlg-${Math.random().toString(36).slice(2, 7)}`,
  },
});

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel']);

// ── Derived IDs ───────────────────────────────────────────────────────────────

const dialogTitleId = computed(() => `${props.dialogId}-title`);
const dialogDescId = computed(() => `${props.dialogId}-desc`);

// ── Icon & variant resolution ─────────────────────────────────────────────────

const VARIANT_ICONS = {
  info: InformationCircleIcon,
  success: CheckCircleIcon,
  warning: ExclamationTriangleIcon,
  danger: XCircleIcon,
  confirm: QuestionMarkCircleIcon,
  delete: TrashIcon,
};

const resolvedVariant = computed(() => props.variant);
const resolvedIcon = computed(() => props.icon ?? VARIANT_ICONS[props.variant]);

// ── Actions ───────────────────────────────────────────────────────────────────

function close() {
  emit('update:modelValue', false);
}

function onConfirm() {
  if (props.loading) return;
  emit('confirm');
}

function onCancel() {
  if (props.loading) return;
  emit('cancel');
  close();
}

function onBackdropClick() {
  if (props.closeOnBackdrop && !props.loading) {
    onCancel();
  }
}
</script>

<style scoped>
/* ── Backdrop ─────────────────────────────────────────────────────────────── */

.app-dialog-backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: rgb(2 6 23 / 0.55);
  backdrop-filter: blur(6px);
}

/* ── Panel ────────────────────────────────────────────────────────────────── */

.app-dialog-panel {
  position: relative;
  width: 100%;
  max-width: 26rem;
  background: #fff;
  border-radius: 28px;
  padding: 2rem 2rem 1.75rem;
  box-shadow:
    0 24px 80px rgba(15, 23, 42, 0.22),
    0 0 0 1px rgba(15, 23, 42, 0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

/* ── Icon wrapper ─────────────────────────────────────────────────────────── */

.app-dialog-icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  flex-shrink: 0;
}

.app-dialog-icon {
  width: 1.75rem;
  height: 1.75rem;
}

/* Variant colours */
.app-dialog-icon-wrap--info    { background: #eff6ff; color: #3b82f6; }
.app-dialog-icon-wrap--success { background: #ecfdf5; color: #059669; }
.app-dialog-icon-wrap--warning { background: #fffbeb; color: #d97706; }
.app-dialog-icon-wrap--danger  { background: #fef2f2; color: #dc2626; }
.app-dialog-icon-wrap--confirm { background: #ecfdf5; color: #059669; }
.app-dialog-icon-wrap--delete  { background: #fef2f2; color: #dc2626; }

/* ── Header ───────────────────────────────────────────────────────────────── */

.app-dialog-header {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.app-dialog-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #0f172a;
  line-height: 1.3;
}

.app-dialog-message {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.6;
}

/* ── Slot ─────────────────────────────────────────────────────────────────── */

.app-dialog-slot {
  width: 100%;
  text-align: left;
}

/* ── Actions ──────────────────────────────────────────────────────────────── */

.app-dialog-actions {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  width: 100%;
  margin-top: 0.5rem;
}

@media (min-width: 480px) {
  .app-dialog-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .app-dialog-actions--single {
    grid-template-columns: 1fr;
  }
}

.app-dialog-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6875rem 1.25rem;
  border-radius: 14px;
  font-size: 0.875rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition:
    background 0.15s ease,
    box-shadow 0.15s ease,
    opacity 0.15s ease,
    transform 0.1s ease;
  line-height: 1.2;
  white-space: normal;
  text-align: center;
}

.app-dialog-btn:active:not(:disabled) {
  transform: scale(0.97);
}

.app-dialog-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

/* Cancel */
.app-dialog-btn--cancel {
  background: #f8fafc;
  color: #475569;
  border: 1.5px solid #e2e8f0;
}

.app-dialog-btn--cancel:hover:not(:disabled) {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* Confirm — variant colours */
.app-dialog-btn--info {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 4px 14px rgb(59 130 246 / 0.35);
}
.app-dialog-btn--info:hover:not(:disabled) { background: #2563eb; }

.app-dialog-btn--success {
  background: #059669;
  color: #fff;
  box-shadow: 0 4px 14px rgb(5 150 105 / 0.35);
}
.app-dialog-btn--success:hover:not(:disabled) { background: #047857; }

.app-dialog-btn--warning {
  background: #d97706;
  color: #fff;
  box-shadow: 0 4px 14px rgb(217 119 6 / 0.35);
}
.app-dialog-btn--warning:hover:not(:disabled) { background: #b45309; }

.app-dialog-btn--danger,
.app-dialog-btn--delete {
  background: #dc2626;
  color: #fff;
  box-shadow: 0 4px 14px rgb(220 38 38 / 0.35);
}
.app-dialog-btn--danger:hover:not(:disabled),
.app-dialog-btn--delete:hover:not(:disabled) { background: #b91c1c; }

.app-dialog-btn--confirm {
  background: #059669;
  color: #fff;
  box-shadow: 0 4px 14px rgb(5 150 105 / 0.35);
}
.app-dialog-btn--confirm:hover:not(:disabled) { background: #047857; }

/* ── Spinner ──────────────────────────────────────────────────────────────── */

.app-dialog-spinner {
  display: inline-block;
  width: 0.875rem;
  height: 0.875rem;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: app-dialog-spin 0.65s linear infinite;
  flex-shrink: 0;
}

@keyframes app-dialog-spin {
  to { transform: rotate(360deg); }
}

/* ── Transition ───────────────────────────────────────────────────────────── */

.app-dialog-enter-active {
  transition: opacity 0.2s ease;
}
.app-dialog-enter-active .app-dialog-panel {
  transition: opacity 0.2s ease, transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.app-dialog-leave-active {
  transition: opacity 0.18s ease;
}
.app-dialog-leave-active .app-dialog-panel {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.app-dialog-enter-from {
  opacity: 0;
}
.app-dialog-enter-from .app-dialog-panel {
  opacity: 0;
  transform: scale(0.9) translateY(8px);
}

.app-dialog-leave-to {
  opacity: 0;
}
.app-dialog-leave-to .app-dialog-panel {
  opacity: 0;
  transform: scale(0.95);
}
</style>
