<template>
  <section id="beneficios" class="relative overflow-hidden bg-[#EAF5EC] py-24 lg:py-32">
    <div class="container mx-auto px-6">
      <!-- Topo -->
      <div class="mx-auto mb-16 max-w-4xl text-center">
        <span class="mb-4 inline-block rounded-full bg-white/60 backdrop-blur px-4 py-1.5 text-xs font-bold tracking-widest text-[#2CA961] uppercase">
          PARA QUEM É O CULTIVA
        </span>
        <h2 class="mb-6 text-3xl leading-tight font-black text-slate-900 md:text-4xl lg:text-5xl">
          Construído para quem faz o <span class="text-[#28995E]">mercado acontecer.</span>
        </h2>
        <p class="text-lg leading-relaxed text-slate-800 font-medium">
          O resultado é uma cadeia mais eficiente para todos.
        </p>
      </div>

      <!-- 3 Colunas: Produtor | O Impacto Global | Varejista -->
      <div class="grid gap-8 lg:grid-cols-3 items-stretch">
        
        <!-- Para Produtores -->
        <div class="flex flex-col rounded-[2rem] border border-green-100 bg-white p-8 shadow-xl transition-all hover:-translate-y-1 hover:shadow-2xl">
          <div class="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#2CA961]/10 text-[#2CA961]">
            <i class="pi pi-user text-4xl"></i>
          </div>
          <h3 class="mb-6 text-2xl font-black text-slate-900">Pequenos Produtores</h3>
          <ul class="mb-10 flex flex-col gap-4 flex-1">
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Mais visibilidade
            </li>
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Mais oportunidades
            </li>
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Planejamento da produção
            </li>
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Menos dependência de atravessadores
            </li>
          </ul>
          <!-- Benefício Direto -->
          <div class="rounded-2xl bg-slate-50 p-6 border border-slate-100 mt-auto">
            <div class="flex items-center gap-3 mb-2">
              <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-white shadow-sm border border-slate-100">
                <svg class="h-6 w-6 text-[#2CA961]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
              </div>
              <h4 class="text-lg font-black text-slate-900">Mais vendas</h4>
            </div>
            <p class="text-base text-slate-700 font-medium leading-relaxed">Pequenos produtores ganham acesso a novos compradores.</p>
          </div>
        </div>

        <!-- O Resultado para Todos -->
        <div id="impacto" class="flex flex-col rounded-[2rem] bg-[#2CA961] p-8 shadow-2xl transition-all hover:-translate-y-1 hover:shadow-green-900/20 text-white relative overflow-hidden">
          <div class="absolute -right-10 -top-10 h-64 w-64 rounded-full bg-white/10 blur-3xl"></div>
          <div class="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/20 text-white backdrop-blur-sm shadow-inner">
            <i class="pi pi-arrow-right-arrow-left text-4xl"></i>
          </div>
          <h3 class="mb-4 text-2xl font-black">Cadeia Eficiente</h3>
          <p class="mb-10 text-base font-medium text-green-50 flex-1 leading-relaxed">
            Ao conectar as pontas do mercado, o Cultiva resolve gargalos históricos e gera benefícios que impactam toda a sociedade.
          </p>
          
          <div class="flex flex-col gap-4 mt-auto">
            <div class="rounded-2xl bg-white/10 p-6 backdrop-blur-md border border-white/20">
              <div class="flex items-center gap-3 mb-2">
                <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-white/10 shadow-sm border border-white/20">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
                </div>
                <h4 class="text-lg font-black">Menos desperdício</h4>
              </div>
              <p class="text-base text-green-50 font-medium leading-relaxed">Oferta e demanda mais alinhadas, evitando perdas na cadeia.</p>
            </div>
            <div class="rounded-2xl bg-white/10 p-6 backdrop-blur-md border border-white/20">
              <div class="flex items-center gap-3 mb-2">
                <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-white/10 shadow-sm border border-white/20">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                </div>
                <h4 class="text-lg font-black">Desenvolvimento regional</h4>
              </div>
              <p class="text-base text-green-50 font-medium leading-relaxed">Fortalecimento da economia local e do comércio justo.</p>
            </div>
          </div>
        </div>

        <!-- Para Varejistas -->
        <div class="flex flex-col rounded-[2rem] border border-green-100 bg-white p-8 shadow-xl transition-all hover:-translate-y-1 hover:shadow-2xl">
          <div class="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#2CA961]/10 text-[#2CA961]">
            <i class="pi pi-shop text-4xl"></i>
          </div>
          <h3 class="mb-6 text-2xl font-black text-slate-900">Varejistas</h3>
          <ul class="mb-10 flex flex-col gap-4 flex-1">
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Mais fornecedores
            </li>
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Menor dependência de distribuidores
            </li>
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Melhor abastecimento
            </li>
            <li class="flex items-center gap-3 text-base font-bold text-slate-800">
              <svg class="h-6 w-6 text-[#2CA961] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
              Compras mais eficientes
            </li>
          </ul>
          <!-- Benefício Direto -->
          <div class="rounded-2xl bg-slate-50 p-6 border border-slate-100 mt-auto">
            <div class="flex items-center gap-3 mb-2">
              <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-white shadow-sm border border-slate-100">
                <svg class="h-6 w-6 text-[#2CA961]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
              </div>
              <h4 class="text-lg font-black text-slate-900">Mais opções</h4>
            </div>
            <p class="text-base text-slate-700 font-medium leading-relaxed">Varejistas encontram novos fornecedores mais próximos.</p>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
</script>
