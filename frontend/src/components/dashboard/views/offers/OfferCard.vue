<template>
  <article
    class="group flex h-full flex-col overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-sm transition hover:-translate-y-0.5 hover:border-emerald-200 hover:shadow-lg"
  >
    <div class="flex flex-1 flex-col p-5">
      <div class="flex items-start justify-between gap-4">
        <div class="min-w-0">
          <p class="text-xs font-bold tracking-[0.26em] text-emerald-600 uppercase">Oferta</p>
          <h3 class="mt-2 truncate text-xl font-black tracking-tight text-slate-900">
            {{ capitalize(item.name || '') }}
          </h3>
          <p
            v-if="item.distance_km !== null && item.distance_km !== undefined"
            class="mt-2 truncate text-sm text-slate-500"
          >
            A {{ item.distance_km }} km de distância
          </p>
        </div>
      </div>

      <div
        v-if="imageUrl"
        class="mt-5 overflow-hidden rounded-[22px] border border-slate-200 bg-slate-50"
      >
        <div class="aspect-[4/3] w-full">
          <AppSecureImage
            :src="imageUrl"
            :alt="capitalize(item.name || '')"
            object-fit-class="object-cover"
          />
        </div>
      </div>
      <div v-else class="mt-5 rounded-[22px] border border-dashed border-slate-200 bg-slate-50 p-4">
        <div
          class="flex aspect-[4/3] items-center justify-center rounded-[18px] border border-slate-200 bg-white text-slate-300"
        >
          <div class="text-center">
            <div
              class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-50 text-slate-300"
            >
              <PhotoIcon class="h-7 w-7" />
            </div>
            <p class="mt-3 text-sm font-semibold text-slate-500">Sem foto</p>
          </div>
        </div>
      </div>

      <div class="mt-auto grid gap-3 pt-5 text-sm sm:grid-cols-2">
        <div class="rounded-2xl bg-slate-50 px-4 py-3">
          <p class="text-xs font-semibold tracking-[0.24em] text-slate-400 uppercase">Preço</p>
          <p class="mt-1 text-base font-bold text-slate-900">R$ {{ item.price }}</p>
        </div>

        <div class="rounded-2xl bg-slate-50 px-4 py-3">
          <p class="text-xs font-semibold tracking-[0.24em] text-slate-400 uppercase">Qtd. Disp.</p>
          <p class="mt-1 text-base font-bold text-slate-900">
            {{ availableQuantity }}
          </p>
        </div>
      </div>

      <div class="mt-5 space-y-3">
        <div
          v-if="cartQuantity > 0"
          class="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-700"
        >
          No carrinho: {{ cartQuantity }}
        </div>

        <div class="flex items-center gap-2">
          <button
            type="button"
            class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-bold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="isAdding || selectedQuantity <= 1 || availableQuantity <= 0"
            @click="decrementQuantity"
          >
            -
          </button>

          <label class="sr-only" :for="`offer-quantity-${item.id}`">Quantidade</label>
          <input
            :id="`offer-quantity-${item.id}`"
            v-model.number="selectedQuantity"
            type="number"
            min="1"
            :max="availableQuantity > 0 ? availableQuantity : 1"
            class="w-20 rounded-xl border border-slate-200 bg-white px-3 py-2 text-center text-sm font-bold text-slate-900 transition outline-none focus:border-emerald-300 focus:ring-4 focus:ring-emerald-100 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="isAdding || availableQuantity <= 0"
            @blur="normalizeQuantity"
          />

          <button
            type="button"
            class="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-bold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="isAdding || availableQuantity <= 0 || selectedQuantity >= availableQuantity"
            @click="incrementQuantity"
          >
            +
          </button>
        </div>

        <button
          type="button"
          class="w-full rounded-2xl bg-emerald-600 px-4 py-3 text-sm font-extrabold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          :disabled="!canAddToCart"
          @click="handleAddToCart"
        >
          {{ isAdding ? 'Adicionando...' : 'Adicionar ao Carrinho' }}
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { PhotoIcon } from '@heroicons/vue/24/outline';
import AppSecureImage from '@/components/ui/AppSecureImage.vue';
import { capitalize } from '@/utils/string';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  cartQuantity: {
    type: Number,
    default: 0,
  },
  isAdding: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['add-to-cart']);
const selectedQuantity = ref(1);

const imageUrl = computed(() => {
  return props.item.images?.[0]?.image || null;
});

const availableQuantity = computed(() => {
  const total = Number(props.item.total_quantity || 0);
  const reserved = Number(props.item.reserved_quantity || 0);
  return Math.max(0, total - reserved);
});

const canAddToCart = computed(() => {
  return (
    !props.isAdding &&
    availableQuantity.value > 0 &&
    selectedQuantity.value > 0 &&
    selectedQuantity.value <= availableQuantity.value
  );
});

function normalizeQuantity() {
  const nextValue = Number(selectedQuantity.value || 0);

  if (!Number.isFinite(nextValue) || nextValue < 1) {
    selectedQuantity.value = 1;
    return;
  }

  if (nextValue > availableQuantity.value && availableQuantity.value > 0) {
    selectedQuantity.value = availableQuantity.value;
  }
}

function incrementQuantity() {
  if (availableQuantity.value <= 0) {
    return;
  }

  selectedQuantity.value = Math.min(selectedQuantity.value + 1, availableQuantity.value);
}

function decrementQuantity() {
  selectedQuantity.value = Math.max(1, selectedQuantity.value - 1);
}

function handleAddToCart() {
  normalizeQuantity();

  if (!canAddToCart.value) {
    return;
  }

  emit('add-to-cart', {
    product: props.item,
    quantity: selectedQuantity.value,
  });
}

watch(availableQuantity, (nextAvailable) => {
  if (nextAvailable <= 0) {
    selectedQuantity.value = 1;
    return;
  }

  if (selectedQuantity.value > nextAvailable) {
    selectedQuantity.value = nextAvailable;
  }
});
</script>
