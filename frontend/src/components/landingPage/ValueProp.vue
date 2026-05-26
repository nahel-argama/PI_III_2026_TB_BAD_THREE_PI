<template>
  <section id="por-que-escolher" class="bg-white py-24">
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
            <i :class="[value.icon, 'text-2xl']" />
          </template>
        </ValueCard>
      </div>
    </div>
  </section>
</template>

<script setup>
import ValueCard from './valueprop/ValueCard.vue';
import 'primeicons/primeicons.css';

const values = [
  {
    title: 'Margens Reais',
    description:
      'Eliminamos o atravessador para que o lucro da venda fique com quem produz, não com quem intermedia.',
      icon: 'pi pi-chart-bar',
  },
  {
    title: 'Georreferenciamento',
    description:
      'Algoritmos que priorizam o comércio local, ajudando tanto o varejista quanto o produtor',
      icon: 'pi pi-map-marker'
  },
  {
    title: 'Preço Dinâmico',
    description:
      'O scrapper de preço dinamico calcula uma media de preços, garantindo competitividade não predatoria.',
      icon: 'pi pi-wallet',
  },
  {
    title: 'Transparencia',
    description:
      'Informação de mercado clara para o pequeno produtor ficar por dentro do mundo agricola.',
      icon: 'pi pi-info-circle',
  },
];
</script>
