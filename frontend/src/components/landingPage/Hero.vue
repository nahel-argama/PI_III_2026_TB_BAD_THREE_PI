<template>
  <section class="relative overflow-hidden bg-white pt-12 pb-24 lg:pt-20 lg:pb-32">
    <div
      class="absolute top-0 right-0 h-[600px] w-[600px] translate-x-1/4 -translate-y-1/2 rounded-full bg-green-50 opacity-60 blur-3xl"
    ></div>

    <div class="relative z-10 container mx-auto px-6">
      <div class="lg:grid lg:grid-cols-2 lg:items-center lg:gap-16">
        <div class="max-w-2xl text-center lg:text-left">
          <span
            class="mb-6 inline-block rounded-full bg-green-100 px-4 py-1.5 text-xs font-black tracking-widest text-green-700 uppercase"
          >
            Logística Inteligente B2B
          </span>

          <h1 class="mb-8 text-5xl leading-[1.1] font-black text-slate-900 lg:text-7xl">
            Do seu campo direto para a
            <span class="text-green-600 underline decoration-green-200 underline-offset-8"
              >prateleira.</span
            >
          </h1>

          <p class="mx-auto mb-10 max-w-xl text-xl leading-relaxed text-slate-600 lg:mx-0">
            O <span class="font-bold text-slate-800">Cultiva</span> elimina atravessadores e conecta
            o pequeno produtor ao varejo local através do nosso website.
          </p>

          <div class="flex flex-col justify-center gap-4 sm:flex-row lg:justify-start">
            <router-link
              to="/register"
              class="rounded-2xl bg-green-600 px-10 py-4 text-lg font-extrabold text-white shadow-xl shadow-green-100 transition-all hover:-translate-y-1 hover:bg-green-700"
            >
              Sou Produtor
            </router-link>
            <router-link
              to="/register"
              class="rounded-2xl border-2 border-slate-200 bg-white px-10 py-4 text-lg font-extrabold text-slate-700 transition-all hover:border-green-600"
            >
              Sou Varejista
            </router-link>
          </div>
        </div>

        <div class="relative mt-16 lg:mt-0">
          <div class="group relative rotate-1 overflow-hidden rounded-[2.5rem] shadow-2xl">
            <img
              src="https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&q=80"
              alt="Produção agrícola fresca"
              class="h-137 w-full object-cover transition-transform duration-700 group-hover:scale-105"
            />

            <div
              class="absolute bottom-8 left-8 -rotate-1 rounded-2xl border border-white/20 bg-white/95 p-5 shadow-2xl backdrop-blur"
            >
              <div class="flex items-center gap-4">
                <div class="rounded-xl bg-orange-100 p-3 text-orange-600">
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="3"
                      d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                    />
                  </svg>
                </div>
                <div>
                  <p class="text-sm leading-none font-black text-slate-900 italic">
                    media de preços
                  </p>
                  <p class="mt-1 text-xs text-slate-500">
                    Preços otimizados com dados da plataforma
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup></script>
