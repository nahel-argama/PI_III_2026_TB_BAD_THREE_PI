<template>
  <section id="processo" class="overflow-hidden bg-slate-50 py-24">
    <div class="container mx-auto px-6">
      <div class="mx-auto mb-20 max-w-3xl text-center">
        <span class="text-sm font-bold tracking-wider text-green-600 uppercase">Como Funciona</span>
        <h2 class="mt-4 mb-6 text-3xl font-black tracking-tight text-slate-900 md:text-5xl">
          Transparência e eficiência em cada etapa
        </h2>
        <p class="text-lg leading-relaxed text-slate-600">
          O fluxo do <span class="font-bold text-slate-800">bad three π</span> foi desenhado para
          eliminar a burocracia, conectar as pontas da cadeia e maximizar o lucro de quem realmente
          produz o alimento.
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
    title: 'Descoberta Local',
    description:
      'Através do nosso sistema de georreferenciamento, o varejista encontra produtores num raio de proximidade ideal, reduzindo os custos logísticos e a pegada de carbono.',
    theme: 'green',
  },
  {
    number: 2,
    title: 'media de preços',
    description:
      'Nosso algoritmo analisa o mercado e sugere o preço ideal em tempo real. Evitamos a concorrência predatória e garantimos que o produtor receba o valor justo pela sua colheita.',
    theme: 'dark',
  },
  {
    number: 3,
    title: 'Conexão Direta',
    description:
      'A negociação e o pedido são efetuados sem intermediários. O ponto de venda recebe produtos mais frescos e o agricultor aumenta a sua margem de lucro em cada transação.',
    theme: 'green',
  },
];
</script>
