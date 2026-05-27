<template>
  <header
    class="group relative isolate min-h-[230px] overflow-hidden rounded-[30px] border border-emerald-100/60 bg-emerald-900 shadow-[0_28px_90px_rgba(6,78,59,0.24)]"
  >
    <img
      v-if="showBannerImage"
      :src="bannerSrc"
      alt="Imagem de capa do perfil"
      class="absolute inset-0 h-full w-full object-cover object-center transition duration-700 group-hover:scale-[1.03]"
      @error="bannerFailed = true"
    />
    <div
      v-else
      class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(110,231,183,0.4)_0,transparent_44%),linear-gradient(130deg,#134e4a_0%,#064e3b_52%,#052e2b_100%)]"
    ></div>

    <div
      class="absolute inset-0 bg-gradient-to-t from-slate-950/88 via-slate-900/58 to-slate-950/35"
    ></div>

    <div class="relative flex min-h-[230px] items-end p-5 sm:p-6 md:p-8">
      <div class="flex w-full flex-col items-center gap-4 sm:flex-row sm:items-end sm:gap-5">
        <div
          class="h-24 w-24 overflow-hidden rounded-full border-4 border-white/85 bg-emerald-50 shadow-[0_18px_45px_rgba(2,6,23,0.35)] sm:h-28 sm:w-28"
        >
          <img
            v-if="avatarSrc && !avatarFailed"
            :src="avatarSrc"
            alt="Foto do usuário"
            class="h-full w-full object-cover"
            @error="avatarFailed = true"
          />
          <div
            v-else
            class="flex h-full w-full items-center justify-center bg-gradient-to-br from-emerald-200 via-emerald-100 to-teal-100 text-2xl font-black text-emerald-800 sm:text-3xl"
          >
            {{ initials }}
          </div>
        </div>

        <div class="pb-1 text-center sm:text-left">
          <h2
            class="max-w-full text-2xl font-black tracking-tight break-words text-white sm:text-3xl"
          >
            {{ name || 'Usuário Cultiva' }}
          </h2>
          <p class="mt-1 text-sm font-semibold text-emerald-100/95 sm:text-base">
            {{ userType || 'Tipo de usuário não informado' }}
          </p>
          <p class="mt-0.5 text-sm text-slate-100/90 sm:text-base">
            {{ location || 'Localização não informada' }}
          </p>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  name: {
    type: String,
    default: '',
  },
  userType: {
    type: String,
    default: '',
  },
  location: {
    type: String,
    default: '',
  },
  bannerSrc: {
    type: String,
    default: '/Hero_image.jpg',
  },
  avatarSrc: {
    type: String,
    default: '',
  },
});

const bannerFailed = ref(false);
const avatarFailed = ref(false);

const showBannerImage = computed(() => Boolean(props.bannerSrc) && !bannerFailed.value);
const initials = computed(() => {
  if (!props.name) return '?';

  return props.name
    .trim()
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('');
});
</script>
