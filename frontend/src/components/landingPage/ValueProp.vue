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
    title: 'Mapeamento Inteligente',
    description:
      'Conecta varejistas aos produtores locais mais próximos usando algoritmos de georreferenciamento. Isso reduz custos logísticos, acelera entregas e fortalece a economia da sua região com total eficiência.',
    icon: 'pi pi-map-marker',
  },
  {
    title: 'Precificação Inteligente',
    description:
      'Motor dinâmico baseado em inteligência de mercado e dados públicos da CONAB. A plataforma sugere preços justos e competitivos, evitando concorrência predatória e garantindo transparência para todos.',
    icon: 'pi pi-dollar',
  },
  {
    title: 'Previsão de Produção',
    description:
      'A partir das listas de interesse do varejo, nosso sistema gera previsões precisas de demanda. Assim, orientamos o produtor sobre o que plantar e quais produtos terão maior potencial e garantia de vendas.',
    icon: 'pi pi-chart-line',
  },
  {
    title: 'Ecossistema Inteligente B2B',
    description:
      'Mais do que um simples marketplace, oferecemos uma infraestrutura tecnológica completa. Nossa plataforma unifica a gestão, comercialização e rastreabilidade em um ambiente acessível, moderno e muito prático.',
    icon: 'pi pi-globe',
  },
];
</script>
