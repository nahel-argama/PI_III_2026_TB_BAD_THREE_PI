<template>
  <div
    class="app-toast"
    :class="[
      `app-toast--${type}`,
      { 'app-toast--hovered': isHovered },
      customClass
    ]"
    :style="{ opacity: dynamicOpacity }"
    :role="type === 'error' || type === 'warning' ? 'alert' : 'status'"
    :aria-live="type === 'error' || type === 'warning' ? 'assertive' : 'polite'"
    tabindex="0"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    @keydown.escape="close"
  >
    <!-- Severity Icon -->
    <div class="app-toast__icon-wrapper" aria-hidden="true">
      <slot name="icon">
        <i :class="['app-toast__icon', iconClass]"></i>
      </slot>
    </div>

    <!-- Main Content -->
    <div class="app-toast__content">
      <div class="app-toast__header">
        <h4 class="app-toast__title">
          <slot name="title">{{ title }}</slot>
        </h4>
      </div>
      <p class="app-toast__description">
        <slot>{{ description }}</slot>
      </p>

      <!-- Contextual Action Button -->
      <div v-if="action" class="app-toast__actions">
        <button
          type="button"
          class="app-toast__action-btn"
          @click.stop="handleAction"
        >
          {{ action.label }}
        </button>
      </div>
    </div>

    <!-- Dismiss Button -->
    <button
      type="button"
      class="app-toast__close-btn"
      aria-label="Fechar notificação"
      @click.stop="close"
    >
      <i class="pi pi-times"></i>
    </button>

    <!-- Visual Countdown Progress Bar -->
    <div class="app-toast__progress-track" aria-hidden="true">
      <div
        class="app-toast__progress-bar"
        :style="{ transform: `scaleX(${duration > 0 ? progressPercentage / 100 : 1})` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  /** Unique identifier for the toast */
  id: {
    type: String,
    required: true,
  },
  /** Toast visual/semantic type: 'success' | 'error' | 'warning' | 'info' */
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value),
  },
  /** Main toast title */
  title: {
    type: String,
    required: true,
  },
  /** Detailed description of the notification event */
  description: {
    type: String,
    default: '',
  },
  /** Duration in milliseconds before automatic closure. 0 disables auto-dismiss */
  duration: {
    type: Number,
    default: 5000,
  },
  /** Additional action button descriptor: { label: string, onClick: Function } */
  action: {
    type: Object,
    default: null,
  },
  /** Ad-hoc custom CSS class wrapper for overrides */
  customClass: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['close', 'action-click']);

// ── State ─────────────────────────────────────────────────────────────────────

const isHovered = ref(false);
// eslint-disable-next-line vue/no-setup-props-reactivity-loss
const remainingTime = ref(props.duration);

let timerId = null;
let lastTick = null;

// ── Computed ──────────────────────────────────────────────────────────────────

/** Maps the toast severity class to a matching PrimeIcon indicator */
const iconClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'pi pi-check-circle app-toast__icon--success';
    case 'error':
      return 'pi pi-times-circle app-toast__icon--error';
    case 'warning':
      return 'pi pi-exclamation-triangle app-toast__icon--warning';
    case 'info':
    default:
      return 'pi pi-info-circle app-toast__icon--info';
  }
});

/** Calculates the exact percentage remaining for progress bar execution */
const progressPercentage = computed(() => {
  if (props.duration <= 0) return 0;
  return Math.min(100, Math.max(0, (remainingTime.value / props.duration) * 100));
});

/** Calculates the dynamic opacity when the toast is in its last 15% of duration */
const dynamicOpacity = computed(() => {
  if (isHovered.value) return 1;
  if (props.duration <= 0) return 1;
  const pct = progressPercentage.value;
  if (pct > 15) return 1;
  return pct / 15; // Linear fade from 100% to 0% in the last 15% of duration
});

// ── Methods ───────────────────────────────────────────────────────────────────

/** Triggers the main closing routine */
function close() {
  emit('close', props.id);
}

/** Handles user interaction with the premium action button */
function handleAction() {
  if (props.action && typeof props.action.onClick === 'function') {
    props.action.onClick(props);
  }
  emit('action-click', props.id);
  close();
}

/** Pixel-perfect time-tracking loop using requestAnimationFrame.
 * Automatically halts progress updates when hovered to prevent unwanted timeout closures.
 */
function tick() {
  if (remainingTime.value <= 0) {
    close();
    return;
  }

  const now = Date.now();
  const delta = now - (lastTick || now);
  lastTick = now;

  if (!isHovered.value) {
    remainingTime.value = Math.max(0, remainingTime.value - delta);
  }

  timerId = requestAnimationFrame(tick);
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────

onMounted(() => {
  if (props.duration > 0) {
    lastTick = Date.now();
    timerId = requestAnimationFrame(tick);
  }
});

onBeforeUnmount(() => {
  if (timerId) {
    cancelAnimationFrame(timerId);
  }
});
</script>

<style scoped>
/* ── Container Layout & Glassmorphism ────────────────────────────────────────── */
.app-toast {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  max-width: 400px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow:
    0 4px 6px -1px rgba(15, 23, 42, 0.05),
    0 10px 30px -3px rgba(15, 23, 42, 0.08);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  outline: none;
}

.app-toast:focus-visible {
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.app-toast--hovered {
  transform: translateY(-2px);
  box-shadow:
    0 10px 15px -3px rgba(15, 23, 42, 0.07),
    0 20px 40px -4px rgba(15, 23, 42, 0.12);
  background: rgba(255, 255, 255, 0.95);
}

/* ── Severity Types Styling ────────────────────────────────────────────────── */
.app-toast--success {
  /* Indicação de severidade expressa puramente na barra horizontal inferior */
}

.app-toast--error {
  /* Indicação de severidade expressa puramente na barra horizontal inferior */
}

.app-toast--warning {
  /* Indicação de severidade expressa puramente na barra horizontal inferior */
}

.app-toast--info {
  /* Indicação de severidade expressa puramente na barra horizontal inferior */
}

/* ── Icon Styles ───────────────────────────────────────────────────────────── */
.app-toast__icon-wrapper {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.app-toast__icon {
  font-size: 1.25rem;
  line-height: 1;
}

.app-toast__icon--success {
  color: #10b981;
}

.app-toast__icon--error {
  color: #ef4444;
}

.app-toast__icon--warning {
  color: #f59e0b;
}

.app-toast__icon--info {
  color: #3b82f6;
}

/* ── Content Layout ────────────────────────────────────────────────────────── */
.app-toast__content {
  flex-grow: 1;
  padding-right: 16px;
  min-width: 0;
}

.app-toast__header {
  margin-bottom: 4px;
}

.app-toast__title {
  margin: 0;
  font-family: inherit;
  font-size: 0.9375rem;
  font-weight: 700;
  color: #0f172a; /* Slate 900 */
  line-height: 1.25;
}

.app-toast__description {
  margin: 0;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #475569; /* Slate 600 */
  line-height: 1.4;
  word-wrap: break-word;
  white-space: pre-line;
}

/* ── Action Styles ─────────────────────────────────────────────────────────── */
.app-toast__actions {
  margin-top: 10px;
}

.app-toast__action-btn {
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #334155; /* Slate 700 */
  cursor: pointer;
  transition: all 0.2s ease;
}

.app-toast__action-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #0f172a;
}

.app-toast__action-btn:active {
  transform: scale(0.97);
}

/* ── Dismiss Button ────────────────────────────────────────────────────────── */
.app-toast__close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: #94a3b8; /* Slate 400 */
  cursor: pointer;
  transition: all 0.2s ease;
}

.app-toast__close-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.app-toast__close-btn i {
  font-size: 0.75rem;
}

/* ── Premium Progress Bar ───────────────────────────────────────────────────── */
.app-toast__progress-track {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(0, 0, 0, 0.05);
}

.app-toast__progress-bar {
  height: 100%;
  width: 100%;
  transform-origin: left center;
  transition: none; /* Evita que a barra sofra lag em relação ao loop de requestAnimationFrame */
}

.app-toast--success .app-toast__progress-bar {
  background: #10b981;
}

.app-toast--error .app-toast__progress-bar {
  background: #ef4444;
}

.app-toast--warning .app-toast__progress-bar {
  background: #f59e0b;
}

.app-toast--info .app-toast__progress-bar {
  background: #3b82f6;
}
</style>
