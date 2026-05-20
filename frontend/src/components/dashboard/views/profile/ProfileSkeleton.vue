<template>
  <section class="space-y-6 pb-6">
    <!-- Skeleton do header -->
    <div
      class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6"
    >
      <div class="flex items-center gap-4">
        <div class="h-16 w-16 shrink-0 animate-pulse rounded-2xl bg-slate-200"></div>
        <div class="flex flex-col gap-2">
          <div class="h-3 w-20 animate-pulse rounded-full bg-emerald-100"></div>
          <div class="h-6 w-48 animate-pulse rounded-full bg-slate-200"></div>
          <div class="h-3 w-36 animate-pulse rounded-full bg-slate-100"></div>
        </div>
      </div>
    </div>

    <!-- Skeleton dos cards -->
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div
        v-for="n in 2"
        :key="n"
        class="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur sm:p-6"
      >
        <div class="mb-5 flex items-center gap-3">
          <div class="h-9 w-9 animate-pulse rounded-xl bg-slate-100"></div>
          <div class="h-4 w-32 animate-pulse rounded-full bg-slate-200"></div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="i in 4" :key="i" class="flex flex-col gap-2">
            <div class="h-2.5 w-20 animate-pulse rounded-full bg-slate-100"></div>
            <div class="h-4 w-28 animate-pulse rounded-full bg-slate-200"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
