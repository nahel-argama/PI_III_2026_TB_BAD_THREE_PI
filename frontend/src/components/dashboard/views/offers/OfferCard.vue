<template>
  <article class="group overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-sm transition hover:-translate-y-0.5 hover:border-emerald-200 hover:shadow-lg">
    <div class="p-5">
      <div class="flex items-start justify-between gap-4">
        <div class="min-w-0">
          <p class="text-xs font-bold uppercase tracking-[0.26em] text-emerald-600">
            Oferta
          </p>
          <h3 class="mt-2 truncate text-xl font-black tracking-tight text-slate-900">
            {{ item.productName }}
          </h3>
          <p class="mt-2 truncate text-sm text-slate-500">
            {{ item.supplierName }} • {{ item.supplierLocation }}
          </p>
        </div>
      </div>

      <div class="mt-5 rounded-[22px] border border-dashed border-slate-200 bg-slate-50 p-4">
        <div class="flex aspect-[4/3] items-center justify-center rounded-[18px] border border-slate-200 bg-white text-slate-300">
          <div class="text-center">
            <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-50 text-slate-300">
              <PhotoIcon class="h-7 w-7" />
            </div>
            <p class="mt-3 text-sm font-semibold text-slate-500">
              Foto em breve
            </p>
          </div>
        </div>
      </div>

      <div class="mt-5 grid gap-3 text-sm sm:grid-cols-2">
        <div class="rounded-2xl bg-slate-50 px-4 py-3">
          <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
            Unidade
          </p>
          <p class="mt-1 text-base font-bold text-slate-900">
            {{ item.unit }}
          </p>
        </div>

        <div class="rounded-2xl bg-slate-50 px-4 py-3">
          <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
            Estoque
          </p>
          <p class="mt-1 text-base font-bold text-slate-900">
            {{ item.stock }}
          </p>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { PhotoIcon } from '@heroicons/vue/24/outline';

defineProps({
  item: {
    type: Object,
    required: true,
  },
});
</script>
