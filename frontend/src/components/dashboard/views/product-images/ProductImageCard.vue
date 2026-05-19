<template>
  <article class="group overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-sm transition hover:-translate-y-0.5 hover:border-emerald-200 hover:shadow-lg">
    <div class="p-5">
      <div class="flex items-start justify-between gap-4">
        <div class="min-w-0">
          <p class="text-xs font-bold uppercase tracking-[0.26em] text-emerald-600">
            Produto
          </p>
          <h3 class="mt-2 truncate text-xl font-black tracking-tight text-slate-900">
            {{ item.name }}
          </h3>
        </div>

        <div class="flex shrink-0 gap-2">
          <button
            type="button"
            class="rounded-2xl border border-slate-200 bg-white p-2.5 text-slate-500 transition hover:border-emerald-200 hover:text-emerald-600"
            :aria-label="`Editar imagem de ${item.name}`"
            @click="$emit('edit', item.id)"
          >
            <PencilSquareIcon class="h-5 w-5" />
          </button>

          <button
            type="button"
            class="rounded-2xl border border-slate-200 bg-white p-2.5 text-slate-500 transition hover:border-rose-200 hover:text-rose-600"
            :aria-label="`Remover ${item.name}`"
            @click="$emit('remove', item.id)"
          >
            <TrashIcon class="h-5 w-5" />
          </button>
        </div>
      </div>

      <div class="mt-5 overflow-hidden rounded-[22px] border border-slate-200 bg-slate-50">
        <div class="aspect-[4/3] w-full">
          <AppSecureImage
            :src="item.imageUrl"
            :alt="item.name"
            object-fit-class="object-cover"
          />
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/outline';
import AppSecureImage from '@/components/ui/AppSecureImage.vue';

defineProps({
  item: {
    type: Object,
    required: true,
  },
});

defineEmits(['edit', 'remove']);
</script>
