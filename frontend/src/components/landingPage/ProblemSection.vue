<template>
  <section id="problema" class="relative bg-white py-24 lg:py-32">
    <div class="container mx-auto px-6">
      <!-- Topo -->
      <div class="mx-auto mb-16 max-w-3xl text-center">
        <span class="mb-4 inline-block rounded-full bg-slate-100 px-4 py-1.5 text-xs font-bold tracking-widest text-slate-600 uppercase">
          O DESAFIO ATUAL
        </span>
        <h2 class="mb-6 text-3xl leading-tight font-black text-slate-900 md:text-4xl lg:text-5xl">
          O mercado ainda funciona de forma <span class="text-[#28995E]">desigual.</span>
        </h2>
        <p class="text-lg leading-relaxed text-slate-800 font-medium">
          Enquanto pequenos produtores enfrentam dificuldades para alcançar novos compradores, varejistas dependem de poucos fornecedores para abastecer seus negócios.
          <br /><br />
          A falta de conexão entre oferta e demanda gera desperdícios, reduz margens e limita oportunidades para ambos os lados.
        </p>
      </div>

      <!-- Cards -->
      <div class="relative grid gap-8 lg:grid-cols-2 lg:gap-16">
        <!-- Elemento Central (Desktop) -->
        <div class="hidden lg:flex absolute left-1/2 top-1/2 z-10 h-16 w-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-white shadow-xl border border-slate-100">
          <svg class="h-8 w-8 text-red-500 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" opacity="0.4"/>
            <line x1="4" y1="4" x2="20" y2="20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>

        <!-- Card Produtor -->
        <div class="group rounded-[2rem] border border-slate-100 bg-slate-50/50 p-8 shadow-xl transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl md:p-10">
          <h3 class="mb-6 text-2xl font-black text-slate-900">Pequeno Produtor</h3>
          <div class="flex flex-col gap-5">
            <div>
              <h4 class="mb-1 text-base font-bold text-slate-900">Baixa Visibilidade</h4>
              <p class="text-base text-slate-700">Dificuldade para encontrar novos compradores além da sua região.</p>
            </div>
            <hr class="border-slate-200" />
            <div>
              <h4 class="mb-1 text-base font-bold text-slate-900">Dependência de Intermediários</h4>
              <p class="text-base text-slate-700">Parte significativa do lucro fica ao longo da cadeia de distribuição.</p>
            </div>
            <hr class="border-slate-200" />
            <div>
              <h4 class="mb-1 text-base font-bold text-slate-900">Falta de Previsibilidade</h4>
              <p class="text-base text-slate-700">Incerteza sobre demanda futura, preços e escoamento da produção.</p>
            </div>
          </div>
        </div>

        <!-- Card Varejista -->
        <div class="group rounded-[2rem] border border-slate-100 bg-slate-50/50 p-8 text-right shadow-xl transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl md:p-10">
          <h3 class="mb-6 text-2xl font-black text-slate-900">Varejista</h3>
          <div class="flex flex-col gap-5">
            <div>
              <h4 class="mb-1 text-base font-bold text-slate-900">Poucas Opções de Fornecedores</h4>
              <p class="text-base text-slate-700">Dependência excessiva de grandes distribuidores.</p>
            </div>
            <hr class="border-slate-200" />
            <div>
              <h4 class="mb-1 text-base font-bold text-slate-900">Custos Elevados</h4>
              <p class="text-base text-slate-700">Preços impactados por múltiplos intermediários.</p>
            </div>
            <hr class="border-slate-200" />
            <div>
              <h4 class="mb-1 text-base font-bold text-slate-900">Dificuldade de Encontrar Produtores Locais</h4>
              <p class="text-base text-slate-700">Falta de acesso a fornecedores próximos e qualificados.</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
</script>
