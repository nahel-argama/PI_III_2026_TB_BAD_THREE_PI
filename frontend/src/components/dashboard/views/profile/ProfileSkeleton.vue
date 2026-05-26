<template>
  <section class="mx-auto w-full max-w-[1120px] space-y-6 pb-6">
    <!-- Skeleton do banner -->
    <div
      class="relative min-h-[230px] overflow-hidden rounded-[30px] border border-emerald-100/60 bg-emerald-900 shadow-[0_28px_90px_rgba(6,78,59,0.24)]"
    >
      <div class="absolute inset-0 animate-pulse bg-slate-700/45"></div>
      <div class="relative flex min-h-[230px] items-end p-5 sm:p-6 md:p-8">
        <div class="flex w-full flex-col items-center gap-4 sm:flex-row sm:items-end sm:gap-5">
          <div
            class="h-24 w-24 shrink-0 animate-pulse rounded-full border-4 border-white/65 bg-slate-200/80 sm:h-28 sm:w-28"
          ></div>
          <div class="flex flex-col items-center gap-2 sm:items-start">
            <div class="h-8 w-52 animate-pulse rounded-full bg-slate-200/80"></div>
            <div class="h-4 w-32 animate-pulse rounded-full bg-slate-100/80"></div>
            <div class="h-4 w-36 animate-pulse rounded-full bg-slate-100/70"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Skeleton do card principal -->
    <div
      class="rounded-[28px] border border-slate-200/85 bg-white p-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] sm:p-7"
    >
      <div class="h-7 w-56 animate-pulse rounded-full bg-slate-200"></div>
      <div class="mt-6 space-y-6">
        <div v-for="section in 3" :key="section">
          <div class="h-3 w-36 animate-pulse rounded-full bg-slate-100"></div>
          <div class="mt-3 grid grid-cols-1 gap-4 md:grid-cols-2">
            <div v-for="field in 2" :key="`section-${section}-field-${field}`" class="space-y-2">
              <div class="h-2.5 w-24 animate-pulse rounded-full bg-slate-100"></div>
              <div class="h-4 w-48 animate-pulse rounded-full bg-slate-200"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
