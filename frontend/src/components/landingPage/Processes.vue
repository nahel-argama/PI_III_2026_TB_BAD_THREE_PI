<template>
  <section id="processo" class="overflow-hidden bg-slate-50 py-24">
    <div class="container mx-auto px-6">
      <div class="mx-auto mb-20 max-w-3xl text-center">
        <span class="text-sm font-bold tracking-wider text-green-600 uppercase">Como Funciona</span>
        <h2 class="mt-4 mb-6 text-3xl font-black tracking-tight text-slate-900 md:text-5xl">
          Transparência, inteligência e eficiência em cada etapa
        </h2>
        <p class="text-lg leading-relaxed text-slate-600">
          O <span class="font-bold text-slate-800">Cultiva</span> conecta pequenos produtores e varejistas através de uma plataforma inteligente que reduz intermediários, otimiza a logística e promove negociações mais justas para toda a cadeia de abastecimento.
        </p>
      </div>

      <div class="relative grid gap-10 md:grid-cols-3">
        <div
          class="absolute top-12 right-[15%] left-[15%] z-0 hidden h-1 rounded-full bg-gradient-to-r from-green-100 via-green-400 to-green-100 opacity-40 md:block"
        ></div>

        <ProcessCard
          v-for="step in stepsData"
          :key="step.number"
          :number="step.number"
          :title="step.title"
          :description="step.description"
          :theme="step.theme"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import ProcessCard from './processes/ProcessesCards.vue';

const stepsData = [
  {
    number: 1,
    title: 'Descoberta Inteligente',
    description:
      'Utilizando georreferenciamento e filtros avançados, o varejista encontra produtores próximos com base em disponibilidade, categoria de produto e capacidade de fornecimento. Isso reduz custos logísticos, acelera entregas e fortalece o comércio local.',
    theme: 'green',
  },
  {
    number: 2,
    title: 'Precificação Dinâmica',
    description:
      'Nosso motor de inteligência de mercado analisa referências públicas, tendências regionais e dados da CONAB para sugerir preços equilibrados em tempo real. O resultado é uma negociação mais transparente, sustentável e sem concorrência predatória.',
    theme: 'green',
  },
  {
    number: 3,
    title: 'Negociação Direta',
    description:
      'A plataforma conecta produtor e varejo sem atravessadores. O varejista amplia sua rede de fornecedores e recebe produtos mais frescos, enquanto o pequeno produtor ganha mais visibilidade, autonomia comercial e margem de lucro.',
    theme: 'green',
  },
];
</script>
