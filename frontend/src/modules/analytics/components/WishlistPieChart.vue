<template>
  <div class="flex h-[400px] w-full justify-center py-6">
    <VueApexCharts
      type="pie"
      width="100%"
      height="100%"
      :options="chartOptions"
      :series="series"
      class="flex w-full max-w-2xl justify-center"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';
import { capitalize } from '@/utils/string';

const props = defineProps({
  results: { type: Array, required: true },
});

const series = computed(() => {
  return props.results?.map((item) => Number(item.total)) || [];
});

const chartOptions = computed(() => {
  return {
    chart: {
      type: 'pie',
      fontFamily: 'inherit',
    },
    labels: props.results?.map((item) => capitalize(item.product_name)) || [],
    tooltip: {
      y: {
        formatter: function (val) {
          return val + ' desejos';
        },
      },
    },
    legend: {
      position: 'bottom',
    },
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 300,
          },
          legend: {
            position: 'bottom',
          },
        },
      },
    ],
  };
});
</script>

<style scoped>
:deep(text.apexcharts-pie-label) {
  /* Animação que mantém a opacidade em 0 durante os primeiros 900ms (64% de 1.4s) e depois faz um fade in até 1 */
  animation: delayAndFade 1.4s ease-in forwards;
}

@keyframes delayAndFade {
  0%,
  64% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
