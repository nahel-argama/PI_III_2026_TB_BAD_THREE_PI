import { ref } from 'vue';

// Global shared state for active toasts.
// Placing this outside of the function body ensures that all components and files
// (including non-SFC JS modules, services, router guards) share the same reactive state.
const activeToasts = ref([]);

let idCounter = 0;

/**
 * useToast - A reactive, fully decoupled composable to trigger premium notifications.
 * Following Clean Code principles, low coupling, and high cohesion.
 */
export function useToast() {
  /**
   * Triggers a generic toast notification.
   * @param {Object} options
   * @param {string} options.title - The bold headline of the notification.
   * @param {string} options.description - Detailed explanation.
   * @param {'success' | 'error' | 'warning' | 'info'} [options.type='info'] - Severity class.
   * @param {number} [options.duration=5000] - Lifespan in milliseconds. 0 disables auto-dismiss.
   * @param {'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center'} [options.position='top-right'] - Placement.
   * @param {Object} [options.action] - Interactive secondary action button.
   * @param {string} options.action.label - Action button text.
   * @param {Function} options.action.onClick - Callback invoked when the user interacts with the action.
   * @param {Function} [options.onOpen] - Callback when the toast mounts in the viewport.
   * @param {Function} [options.onClose] - Callback when the toast is dismissed.
   * @param {string} [options.customClass] - Overriding classes for ad-hoc custom designs.
   * @returns {string} The unique ID of the created toast.
   */
  const show = (options) => {
    const id = `toast-${++idCounter}-${Date.now()}`;
    const duration = options.duration ?? 5000;
    const position = options.position ?? 'top-right';

    const newToast = {
      id,
      title: options.title,
      description: options.description,
      type: options.type || 'info',
      duration,
      position,
      action: options.action,
      onClose: options.onClose,
      onOpen: options.onOpen,
      customClass: options.customClass,
      createdAt: Date.now(),
    };

    activeToasts.value.push(newToast);

    if (typeof options.onOpen === 'function') {
      try {
        options.onOpen(newToast);
      } catch (err) {
        console.error('[useToast] Error inside onOpen callback:', err);
      }
    }

    return id;
  };

  /**
   * Triggers a Success toast notification.
   */
  const success = (description, title = 'Sucesso', options = {}) => {
    return show({ type: 'success', title, description, ...options });
  };

  /**
   * Triggers an Error toast notification.
   */
  const error = (description, title = 'Erro', options = {}) => {
    return show({ type: 'error', title, description, ...options });
  };

  /**
   * Triggers a Warning toast notification.
   */
  const warning = (description, title = 'Atenção', options = {}) => {
    return show({ type: 'warning', title, description, ...options });
  };

  /**
   * Triggers an Info toast notification.
   */
  const info = (description, title = 'Informação', options = {}) => {
    return show({ type: 'info', title, description, ...options });
  };

  /**
   * Dismisses a specific toast from the viewport.
   * @param {string} id - The ID of the toast to dismiss.
   */
  const dismiss = (id) => {
    const index = activeToasts.value.findIndex((t) => t.id === id);
    if (index !== -1) {
      const toast = activeToasts.value[index];
      if (typeof toast.onClose === 'function') {
        try {
          toast.onClose(toast);
        } catch (err) {
          console.error('[useToast] Error inside onClose callback:', err);
        }
      }
      activeToasts.value.splice(index, 1);
    }
  };

  /**
   * Clears the entire notification queue.
   */
  const dismissAll = () => {
    activeToasts.value.forEach((toast) => {
      if (typeof toast.onClose === 'function') {
        try {
          toast.onClose(toast);
        } catch (err) {
          console.error('[useToast] Error inside onClose callback:', err);
        }
      }
    });
    activeToasts.value = [];
  };

  return {
    activeToasts,
    show,
    success,
    error,
    warning,
    info,
    dismiss,
    dismissAll,
  };
}
