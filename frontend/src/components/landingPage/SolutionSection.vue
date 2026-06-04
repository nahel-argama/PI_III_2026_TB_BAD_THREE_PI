<template>
  <section id="como-funciona" class="relative overflow-hidden bg-[#EAF5EC] py-24 lg:py-32">
    <!-- Background Decorativo -->

    <div class="relative z-10 container mx-auto px-6">
      <!-- Topo -->
      <div class="mx-auto mb-16 max-w-3xl text-center">
        <span class="mb-4 inline-block rounded-full bg-white/60 backdrop-blur px-4 py-1.5 text-xs font-bold tracking-widest text-[#2CA961] uppercase">
          COMO FUNCIONA
        </span>
        <h2 class="mb-6 text-3xl leading-tight font-black text-slate-900 md:text-4xl lg:text-5xl">
          Tudo acontece em <span class="text-[#28995E]">poucos passos.</span>
        </h2>
        <p class="text-lg leading-relaxed text-slate-800 font-medium">
          O Cultiva simplifica a conexão entre produtores e varejistas através de um processo intuitivo e orientado por dados.
        </p>
      </div>

      <!-- Timeline Horizontal -->
      <div class="relative mt-20">
        <!-- Linha de conexão visível apenas no desktop -->
        <div class="absolute left-[12%] right-[12%] top-12 hidden h-1.5 rounded-full bg-white/50 lg:block">
          <div class="h-full w-full animate-pulse rounded-full bg-gradient-to-r from-transparent via-[#2CA961] to-transparent"></div>
        </div>

        <div class="grid gap-12 lg:grid-cols-4 lg:gap-8">
          <!-- Passo 1 -->
          <div class="relative flex flex-col items-center text-center group">
            <div class="z-10 mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-white/80 backdrop-blur-xl border border-white p-4 shadow-xl transition-transform duration-300 group-hover:-translate-y-2 group-hover:shadow-2xl">
              <svg class="h-8 w-8 text-[#2CA961]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
              </svg>
            </div>
            <span class="mb-3 text-xs font-black text-[#28995E] uppercase tracking-widest">Passo 1 / Cadastro</span>
            <h3 class="mb-3 text-xl font-black text-slate-900">Cadastre sua produção</h3>
            <p class="text-base text-slate-700 font-medium leading-relaxed">
              Registre produtos, quantidades disponíveis e previsões futuras.
            </p>
          </div>

          <!-- Passo 2 -->
          <div class="relative flex flex-col items-center text-center group">
            <div class="z-10 mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-white/80 backdrop-blur-xl border border-white p-4 shadow-xl transition-transform duration-300 group-hover:-translate-y-2 group-hover:shadow-2xl">
              <svg class="h-8 w-8 text-[#2CA961]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
              </svg>
            </div>
            <span class="mb-3 text-xs font-black text-[#28995E] uppercase tracking-widest">Passo 2 / Oferta e Demanda</span>
            <h3 class="mb-3 text-xl font-black text-slate-900">Informe sua demanda</h3>
            <p class="text-base text-slate-700 font-medium leading-relaxed">
              Varejistas indicam o que precisam comprar e quando precisam receber.
            </p>
          </div>

          <!-- Passo 3 -->
          <div class="relative flex flex-col items-center text-center group">
            <div class="z-10 mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-[#2CA961] border border-white/40 p-4 shadow-xl shadow-green-200 transition-transform duration-300 group-hover:-translate-y-2 group-hover:shadow-2xl">
              <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
              </svg>
            </div>
            <span class="mb-3 text-xs font-black text-[#28995E] uppercase tracking-widest">Passo 3 / Match</span>
            <h3 class="mb-3 text-xl font-black text-slate-900">Receba conexões</h3>
            <p class="text-base text-slate-700 font-medium leading-relaxed">
              A plataforma identifica oportunidades compatíveis para ambos os lados.
            </p>
          </div>

          <!-- Passo 4 -->
          <div class="relative flex flex-col items-center text-center group">
            <div class="z-10 mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-white/80 backdrop-blur-xl border border-white p-4 shadow-xl transition-transform duration-300 group-hover:-translate-y-2 group-hover:shadow-2xl">
              <svg class="h-8 w-8 text-[#2CA961]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
              </svg>
            </div>
            <span class="mb-3 text-xs font-black text-[#28995E] uppercase tracking-widest">Passo 4 / Pedido e Pagamento</span>
            <h3 class="mb-3 text-xl font-black text-slate-900">Negocie e finalize</h3>
            <p class="text-base text-slate-700 font-medium leading-relaxed">
              Pedidos, pagamentos e comprovantes centralizados em um único ambiente.
            </p>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
</script>
