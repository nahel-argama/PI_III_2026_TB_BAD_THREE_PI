<template>
  <section class="bg-white py-24">
    <div class="container mx-auto px-6">
      <div class="mb-16 flex flex-col items-end justify-between gap-8 md:flex-row">
        <div class="max-w-2xl">
          <h2 class="mb-4 text-4xl leading-tight font-black text-slate-900">
            Por que escolher o <span class="text-green-600"> cultiva?</span>
          </h2>
          <p class="text-lg text-slate-600">
            Muito mais do que um marketplace, somos a infraestrutura tecnológica que o pequeno
            produtor precisa para competir no mercado moderno.
          </p>
        </div>
      </div>

      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <ValueCard
          v-for="value in values"
          :key="value.title"
          :title="value.title"
          :description="value.description"
        >
          <template #icon>
            <component :is="value.icon" class="h-6 w-6" />
          </template>
        </ValueCard>
      </div>
    </div>
  </section>
</template>

<script setup>
import ValueCard from './valueprop/ValueCard.vue';

const values = [
  {
    title: 'Margens Reais',
    description:
      'Eliminamos o atravessador para que o lucro da venda fique com quem produz, não com quem intermedia.',
  },
  {
    title: 'Georreferenciamento',
    description:
      'Algoritmos que priorizam o comércio local, ajudando tanto o varejista quanto o produtor',
  },
  {
    title: 'Preço Dinâmico',
    description:
      'O scrapper de preço dinamico equilibra a oferta e procura, garantindo competitividade de preços.',
  },
  {
    title: 'Transparencia',
    description:
      'Informação de mercado clara para o pequeno produtor saber o que e quando plantar para vender melhor.',
  },
];
</script>
