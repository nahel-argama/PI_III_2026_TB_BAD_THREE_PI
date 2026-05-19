<template>
  <article
    class="group overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-sm transition hover:-translate-y-0.5 hover:border-emerald-200 hover:shadow-lg"
  >
    <div class="p-5">
      <div class="flex items-start justify-between gap-4">
        <div class="min-w-0">
          <p class="text-xs font-bold tracking-[0.26em] text-emerald-600 uppercase">
            Produto salvo
          </p>
          <h3 class="mt-2 truncate text-xl font-black tracking-tight text-slate-900">
            {{ capitalize(item.product_name) }}
          </h3>
        </div>

        <button
          type="button"
          class="rounded-2xl border border-slate-200 bg-white p-2.5 text-slate-500 transition hover:border-rose-200 hover:text-rose-600 disabled:cursor-not-allowed disabled:opacity-50"
          :aria-label="`Remover ${capitalize(item.product_name)}`"
          :disabled="isRemoving"
          @click="handleRemove"
        >
          <TrashIcon class="h-5 w-5" />
        </button>
      </div>

      <div
        class="mt-5 flex aspect-[4/3] items-center justify-center rounded-[22px] border border-dashed border-slate-200 bg-slate-50"
      >
        <div class="text-center">
          <div
            class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm"
          >
            <PhotoIcon class="h-7 w-7" />
          </div>
          <p class="mt-3 text-sm font-semibold text-slate-500">Foto em breve</p>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref } from 'vue';
import { PhotoIcon, TrashIcon } from '@heroicons/vue/24/outline';
import { removeProductFromWishlist } from '@/services/wishlist';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['remove']);

const isRemoving = ref(false);

async function handleRemove() {
  isRemoving.value = true;
  try {
    await removeProductFromWishlist(props.item.id);
    emit('remove', props.item.id);
  } catch {
    // Silencia o erro, mantendo o estado do botão
  } finally {
    isRemoving.value = false;
  }
}
</script>
