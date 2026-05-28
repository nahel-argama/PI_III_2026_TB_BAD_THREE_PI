<template>
  <div class="overflow-x-auto">
    <table class="w-full text-left text-sm text-slate-600">
      <thead class="border-b border-slate-100 text-xs font-semibold uppercase text-slate-500">
        <tr>
          <th class="px-6 py-5">Pos</th>
          <th class="px-6 py-5">Produto</th>
          <th class="px-6 py-5">Quantidade</th>
          <th class="px-6 py-5">Participação</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        <tr v-for="(item, index) in results" :key="item.product_external_key" class="hover:bg-slate-50/50 transition">
          <td class="px-6 py-4 font-semibold" :class="[
            index === 0 ? 'text-amber-500' : '',
            index === 1 ? 'text-slate-400' : '',
            index === 2 ? 'text-orange-400' : '',
            index > 2 ? 'text-slate-400 font-normal' : ''
          ]">
            <span>#{{ index + 1 }}</span>
          </td>
          <td class="px-6 py-4 font-medium text-slate-800">
            {{ capitalize(item.product_name) }}
          </td>
          <td class="px-6 py-4">
            {{ item.total }} desejos
          </td>
          <td class="px-6 py-4">
            <div class="flex items-center gap-3">
              <span class="w-10 font-medium">{{ item.percentage }}%</span>
              <div class="h-2 w-24 rounded-full bg-slate-200 sm:w-32">
                <div
                  class="h-full rounded-full bg-emerald-500"
                  :style="`width: ${item.percentage}%`"
                ></div>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  results: { type: Array, required: true }
});
</script>
