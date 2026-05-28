<template>
  <div class="flex justify-center py-6 h-[400px]">
    <v-chart class="w-full h-full" :option="chartOption" autoresize />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

const props = defineProps({
  results: { type: Array, required: true }
});

const chartOption = computed(() => {
  if (!props.results?.length) return {};
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: <br/>{c} desejos ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll',
    },
    series: [
      {
        name: 'Produtos Desejados',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: props.results.map(item => ({
          value: item.total,
          name: item.product_name
        }))
      }
    ]
  };
});
</script>
