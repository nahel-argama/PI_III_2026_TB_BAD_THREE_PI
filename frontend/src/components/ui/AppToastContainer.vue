<template>
  <Teleport to="body">
    <!-- Render containers dynamically only for positions that currently have active notifications -->
    <div
      v-for="position in activePositions"
      :key="position"
      :class="['app-toast-container', `app-toast-container--${position}`]"
    >
      <TransitionGroup name="app-toast-list" tag="div" class="app-toast-container__stack">
        <AppToast
          v-for="toast in toastsByPosition[position]"
          :id="toast.id"
          :key="toast.id"
          :type="toast.type"
          :title="toast.title"
          :description="toast.description"
          :duration="toast.duration"
          :action="toast.action"
          :custom-class="toast.customClass"
          @close="dismiss"
        />
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue';
import { useToast } from '@/composables/useToast';
import AppToast from './AppToast.vue';

const { activeToasts, dismiss } = useToast();

// ── Computed ──────────────────────────────────────────────────────────────────

/** Groups all active notifications by screen coordinate alignment */
const toastsByPosition = computed(() => {
  const groups = {
    'top-left': [],
    'top-center': [],
    'top-right': [],
    'bottom-left': [],
    'bottom-center': [],
    'bottom-right': [],
  };

  activeToasts.value.forEach((toast) => {
    const pos = toast.position || 'top-right';
    if (groups[pos]) {
      groups[pos].push(toast);
    } else {
      groups['top-right'].push(toast);
    }
  });

  return groups;
});

/** Lists coordinate keys that actively contain one or more notifications */
const activePositions = computed(() => {
  return Object.keys(toastsByPosition.value).filter(
    (pos) => toastsByPosition.value[pos].length > 0,
  );
});
</script>

<style scoped>
/* ── Container Layouts ───────────────────────────────────────────────────────── */
.app-toast-container {
  position: fixed;
  z-index: 10000; /* Overrides any navigation bars, modals, or page elements */
  pointer-events: none; /* Allows mouse interactions to bypass container background */
  display: flex;
  flex-direction: column;
  padding: 24px;
  width: 100%;
  max-width: 448px; /* Restricts maximum expansion */
  box-sizing: border-box;
}

.app-toast-container__stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

/* ── Positional Anchor Alignments ────────────────────────────────────────────── */
.app-toast-container--top-left {
  top: 0;
  left: 0;
}

.app-toast-container--top-center {
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  align-items: center;
}

.app-toast-container--top-right {
  top: 0;
  right: 0;
}

.app-toast-container--bottom-left {
  bottom: 0;
  left: 0;
}

.app-toast-container--bottom-center {
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  align-items: center;
}

.app-toast-container--bottom-right {
  bottom: 0;
  right: 0;
}

/* Enable pointer events only for individual Toast elements inside the containers */
.app-toast-container :deep(.app-toast) {
  pointer-events: auto;
}

/* ── Premium List Transitions ────────────────────────────────────────────────── */
.app-toast-list-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); /* Bouncy elastic curve na entrada */
}

.app-toast-list-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease; /* Transição suave de fade e escala na saída, sem bounce */
}

/* Standard opacity and dynamic transforms based on location */
.app-toast-list-enter-from {
  opacity: 0;
}

/* Top positions slide down on entry */
.app-toast-container--top-left .app-toast-list-enter-from,
.app-toast-container--top-right .app-toast-list-enter-from {
  transform: translateY(-24px) scale(0.92);
}

.app-toast-container--top-center .app-toast-list-enter-from {
  transform: translateY(-24px) scale(0.92);
}

/* Bottom positions slide up on entry */
.app-toast-container--bottom-left .app-toast-list-enter-from,
.app-toast-container--bottom-right .app-toast-list-enter-from {
  transform: translateY(24px) scale(0.92);
}

.app-toast-container--bottom-center .app-toast-list-enter-from {
  transform: translateY(24px) scale(0.92);
}

/* Leave transition: elegant collapse and fadeout */
.app-toast-list-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Ensure active sibling elements move smoothly when a target toast leaves */
.app-toast-list-leave-active {
  position: absolute;
  width: calc(100% - 48px); /* Matches exact width inside padding */
}

.app-toast-container--top-center .app-toast-list-leave-active,
.app-toast-container--bottom-center .app-toast-list-leave-active {
  width: 100%;
}

.app-toast-list-move {
  transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
</style>
