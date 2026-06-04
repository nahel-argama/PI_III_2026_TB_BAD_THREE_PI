<template>
  <section class="relative overflow-hidden bg-[#EAF5EC] pt-12 pb-24 lg:pt-20 lg:pb-32">
    <div class="relative z-10 container mx-auto px-6">
      <div class="lg:grid lg:grid-cols-2 lg:items-center lg:gap-16">
        <div class="max-w-2xl text-center lg:text-left">
          <h1 class="mb-8 text-5xl leading-[1.15] font-black text-slate-900 lg:text-7xl">
            Do seu campo<br />direto para a<br />
            <span class="relative inline-block text-[#28995E]">
              prateleira.
              <svg
                class="absolute -bottom-3 left-0 w-full"
                viewBox="0 0 200 20"
                preserveAspectRatio="none"
              >
                <path
                  d="M0,15 C50,0 150,20 200,5"
                  stroke="#28995E"
                  stroke-width="5"
                  stroke-linecap="round"
                  fill="none"
                  class="opacity-70"
                />
              </svg>
            </span>
          </h1>

          <p class="mx-auto mb-10 max-w-xl text-xl leading-relaxed text-slate-800 font-medium lg:mx-0">
            O Cultiva elimina atravessadores e conecta
            o pequeno produtor ao varejo local através do nosso website.
          </p>

          <div class="flex flex-col justify-center gap-4 sm:flex-row lg:justify-start">
            <router-link
              to="/register?type=PRODUCER"
              class="rounded-full bg-[#2CA961] px-10 py-4 text-lg font-bold text-white shadow-lg shadow-green-200 transition-all hover:-translate-y-1 hover:bg-[#23874d]"
            >
              Sou Produtor
            </router-link>
            <router-link
              to="/register?type=RETAILER"
              class="rounded-full border-2 border-[#2CA961] bg-white px-10 py-4 text-lg font-bold text-[#2CA961] shadow-lg shadow-slate-100 transition-all hover:-translate-y-1 hover:bg-green-50"
            >
              Sou Varejista
            </router-link>
          </div>
        </div>

        <div class="relative mt-16 lg:mt-0">
          <div class="relative overflow-hidden rounded-[2rem] shadow-2xl">
            <img
              src="/Hero_image.jpg"
              alt="Produção agrícola fresca"
              class="h-[550px] w-full object-cover lg:h-[600px]"
            />
          </div>

          <div
            class="absolute bottom-8 right-8 z-20 w-64 rounded-3xl bg-white/50 backdrop-blur-xl border border-white/40 p-6 shadow-2xl"
          >
            <div class="flex flex-col gap-3">
              <div class="text-[#2CA961]">
                <svg
                  class="h-10 w-10"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M18 20V10M12 20V4M6 20V14" />
                  <path d="M4 14l6-6 4 4 8-8" />
                  <path d="M18 4h4v4" />
                </svg>
              </div>
              <div>
                <p class="text-lg font-bold text-slate-900">Média de preços</p>
                <p class="mt-1 text-sm font-medium text-slate-800 leading-tight">
                  Preços otimizados com<br />dados da plataforma
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup></script>
