<template>
  <article class="overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-sm transition hover:border-emerald-200 hover:shadow-lg">
    <button
      type="button"
      class="flex w-full items-center justify-between gap-4 px-5 py-5 text-left transition hover:bg-slate-50/80"
      :aria-expanded="isOpen"
      @click="$emit('toggle', item.id)"
    >
      <div class="min-w-0 flex-1">
        <div class="flex flex-wrap items-center gap-2">
          <p class="text-xs font-bold uppercase tracking-[0.26em] text-emerald-600">
            {{ itemKindLabel }}
          </p>
          <span
            class="rounded-full px-3 py-1 text-[11px] font-bold uppercase tracking-[0.22em]"
            :class="statusClasses[item.statusTone || 'emerald']"
          >
            {{ item.status }}
          </span>
        </div>

        <h3 class="mt-2 truncate text-xl font-black tracking-tight text-slate-900">
          {{ item.contractTitle }}
        </h3>

        <p class="mt-1 truncate text-sm text-slate-500">
          {{ item.partyName }} • {{ item.date }}
        </p>
      </div>

      <div class="shrink-0 rounded-2xl border border-slate-200 bg-white p-2 text-slate-500">
        <ChevronDownIcon
          class="h-5 w-5 transition duration-300"
          :class="isOpen ? 'rotate-180' : ''"
        />
      </div>
    </button>

    <transition name="history-panel">
      <div
        v-if="isOpen"
        class="border-t border-slate-100 px-5 py-5"
      >
        <div class="space-y-3">
          <div class="min-w-0 space-y-3">
            <div class="rounded-[22px] bg-slate-50 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Fornecedor
              </p>
              <p class="mt-1 text-base font-bold text-slate-900">
                {{ item.partyName }}
              </p>
              <p class="mt-1 text-sm text-slate-500">
                {{ item.partyDocument }} • {{ item.partyLocation }}
              </p>
            </div>

            <div class="rounded-[22px] bg-slate-50 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Contato
              </p>
              <p class="mt-1 text-base font-bold text-slate-900">
                {{ item.partyContact }}
              </p>
              <p class="mt-1 text-sm text-slate-500">
                {{ item.partyEmail }}
              </p>
            </div>

            <div class="rounded-[22px] bg-slate-50 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Data do contrato
              </p>
              <p class="mt-1 text-base font-bold text-slate-900">
                {{ item.date }}
              </p>
            </div>
          </div>
        </div>

        <div class="mt-4 grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
          <div class="rounded-[22px] bg-slate-50 px-4 py-4">
            <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
              Itens {{ itemKindLabel.toLowerCase() }}
            </p>

            <div class="mt-3 space-y-3">
              <div
                v-for="contractItem in item.items"
                :key="contractItem.name"
                class="flex items-center justify-between gap-4 rounded-2xl bg-white px-4 py-3"
              >
                <div class="min-w-0">
                  <p class="truncate text-sm font-bold text-slate-900">
                    {{ contractItem.name }}
                  </p>
                  <p class="mt-1 text-xs text-slate-500">
                    {{ contractItem.quantity }} • {{ contractItem.unit }}
                  </p>
                </div>

                <span class="shrink-0 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                  {{ contractItem.category }}
                </span>
              </div>
            </div>
          </div>

          <div class="space-y-3">
            <div class="rounded-[22px] bg-slate-50 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Forma de pagamento
              </p>
              <p class="mt-1 text-base font-bold text-slate-900">
                {{ item.payment.method }}
              </p>
              <p class="mt-1 text-sm text-slate-500">
                {{ item.payment.details }}
              </p>
            </div>

            <div class="rounded-[22px] bg-slate-50 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Valor do contrato
              </p>
              <p class="mt-1 text-base font-bold text-slate-900">
                {{ item.payment.total }}
              </p>
            </div>

          </div>
        </div>
      </div>
    </transition>
  </article>
</template>

<script setup>
import { ChevronDownIcon } from '@heroicons/vue/24/outline';

defineProps({
  item: {
    type: Object,
    required: true,
  },
  itemKindLabel: {
    type: String,
    required: true,
  },
  isOpen: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['toggle']);

const statusClasses = {
  emerald: 'bg-emerald-50 text-emerald-700',
  amber: 'bg-amber-50 text-amber-700',
  red: 'bg-rose-50 text-rose-700',
  blue: 'bg-sky-50 text-sky-700',
};
</script>

<style scoped>
.history-panel-enter-active,
.history-panel-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}

.history-panel-enter-from,
.history-panel-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
