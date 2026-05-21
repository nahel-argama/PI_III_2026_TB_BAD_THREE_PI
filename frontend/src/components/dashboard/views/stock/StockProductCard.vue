<template>
  <article
    class="group overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-sm transition hover:-translate-y-0.5 hover:border-emerald-200 hover:shadow-lg"
  >
    <div class="p-5">
      <div class="flex items-start justify-between gap-4">
        <div class="min-w-0">
          <h3 class="mt-2 truncate text-xl font-black tracking-tight text-slate-900">
            {{ capitalize(item.name) }}
          </h3>
          <p class="mt-1 text-sm font-medium text-slate-500">
            {{ item.total_quantity }} em estoque | R$ {{ item.price }}
          </p>
        </div>

        <button
          type="button"
          class="rounded-2xl border border-slate-200 bg-white p-2.5 text-slate-500 transition hover:border-rose-200 hover:text-rose-600 disabled:cursor-not-allowed disabled:opacity-50"
          :aria-label="`Remover ${capitalize(item.name)}`"
          :disabled="isRemoving"
          @click="openDeleteDialog"
        >
          <TrashIcon class="h-5 w-5" />
        </button>
      </div>

      <div
        v-if="imageUrl"
        class="mt-5 overflow-hidden rounded-[22px] border border-slate-200 bg-slate-50"
      >
        <div class="aspect-[4/3] w-full">
          <AppSecureImage
            :src="imageUrl"
            :alt="capitalize(item.name)"
            object-fit-class="object-cover"
          />
        </div>
      </div>

      <div
        v-else
        class="mt-5 flex aspect-[4/3] items-center justify-center rounded-[22px] border border-dashed border-slate-200 bg-slate-50"
      >
        <div class="text-center">
          <div
            class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm"
          >
            <PhotoIcon class="h-7 w-7" />
          </div>
          <p class="mt-3 text-sm font-semibold text-slate-500">Imagem não disponível</p>
        </div>
      </div>
    </div>

    <AppDialog
      v-model="isDialogOpen"
      title="Remover produto?"
      :message="`Tem certeza que deseja remover ${capitalize(item.name)} do seu estoque? Esta ação não pode ser desfeita.`"
      variant="danger"
      confirm-label="Remover"
      :loading="isRemoving"
      @confirm="confirmDelete"
    />
  </article>
</template>

<script setup>
import { computed, ref } from 'vue';
import { PhotoIcon, TrashIcon } from '@heroicons/vue/24/outline';
import AppSecureImage from '@/components/ui/AppSecureImage.vue';
import AppDialog from '@/components/ui/AppDialog.vue';
import { deleteProduct } from '@/services/product';
import { capitalize } from '@/utils/string';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['remove']);

const isRemoving = ref(false);
const isDialogOpen = ref(false);

const imageUrl = computed(() => {
  return props.item.images?.[0]?.image || null;
});

function openDeleteDialog() {
  isDialogOpen.value = true;
}

async function confirmDelete() {
  isRemoving.value = true;
  try {
    await deleteProduct(props.item.id);
    emit('remove', props.item.id);
    isDialogOpen.value = false;
  } catch {
    // Silencia o erro, mantendo o estado do botão
  } finally {
    isRemoving.value = false;
  }
}
</script>
