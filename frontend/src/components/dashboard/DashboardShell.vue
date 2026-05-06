<template>
  <div
    class="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.14),_transparent_34%),linear-gradient(180deg,_#f8fafc_0%,_#f1f8f4_100%)] text-slate-900"
  >
    <div class="flex min-h-screen w-full">
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 z-30 bg-slate-950/45 lg:hidden"
        aria-hidden="true"
        @click="$emit('close-sidebar')"
      ></div>

      <aside
        class="fixed inset-y-0 left-0 z-40 w-72 overflow-y-auto border-r border-white/70 bg-white/90 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur-xl transition-transform duration-300 lg:translate-x-0"
        :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
      >
        <slot name="sidebar" />
      </aside>

      <div class="flex min-h-screen w-full flex-1 flex-col lg:ml-72">
        <div class="sticky top-0 z-20 w-full border-b border-white/70 bg-white/70 backdrop-blur-xl">
          <slot name="topbar" />
        </div>

        <main class="flex-1 px-4 pb-5 sm:px-6 lg:px-8">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  sidebarOpen: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['close-sidebar']);
</script>
