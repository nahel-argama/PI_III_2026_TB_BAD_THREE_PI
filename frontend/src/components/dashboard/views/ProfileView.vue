<template>
  <section class="space-y-6 pb-6">
    <!-- Estado de loading -->
    <ProfileSkeleton v-if="isLoading" />

    <!-- Estado de erro -->
    <div
      v-else-if="error"
      class="flex min-h-[calc(100vh-12rem)] items-center justify-center rounded-[28px] border border-dashed border-red-200 bg-red-50/40 p-10"
    >
      <div class="max-w-sm text-center">
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-red-100 text-red-500"
        >
          <ExclamationTriangleIcon class="h-7 w-7" />
        </div>
        <h3 class="text-base font-bold text-slate-800">Erro ao carregar perfil</h3>
        <p class="mt-2 text-sm text-slate-500">{{ error }}</p>
        <button
          type="button"
          class="mt-5 inline-flex items-center gap-2 rounded-2xl bg-emerald-600 px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-emerald-600/25 transition hover:bg-emerald-700"
          @click="load"
        >
          <ArrowPathIcon class="h-4 w-4" />
          Tentar novamente
        </button>
      </div>
    </div>

    <!-- Conteúdo do perfil -->
    <template v-else-if="profile">
      <ProfileBanner
        :name="profile.name"
        :user-type="userTypeLabel"
        :location="cityStateLabel"
        :banner-src="BANNER_IMAGE"
      />

      <AccountInfoCard title="Informações da Conta" :sections="accountSections" />
    </template>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { ExclamationTriangleIcon, ArrowPathIcon } from '@heroicons/vue/24/outline';

import ProfileBanner from './profile/ProfileBanner.vue';
import AccountInfoCard from './profile/AccountInfoCard.vue';
import ProfileSkeleton from './profile/ProfileSkeleton.vue';

import { fetchCurrentUserProfile } from '@/services/profile';
import { formatDocument, formatPostalCode } from '@/utils/formatters';

// ── Props ─────────────────────────────────────────────────────────────────────

const props = defineProps({
  roleLabel: {
    type: String,
    required: true,
  },
});

// ── State ─────────────────────────────────────────────────────────────────────

const profile = ref(null);
const isLoading = ref(false);
const error = ref(null);

// ── Fetch ─────────────────────────────────────────────────────────────────────

async function load() {
  isLoading.value = true;
  error.value = null;

  try {
    profile.value = await fetchCurrentUserProfile();
  } catch {
    error.value = 'Não foi possível carregar os dados do perfil. Tente novamente.';
  } finally {
    isLoading.value = false;
  }
}

onMounted(load);

// ── Computed fields ───────────────────────────────────────────────────────────

const DOCUMENT_TYPE_LABEL = {
  CPF: 'CPF',
  CNPJ: 'CNPJ',
};

const USER_TYPE_LABEL = {
  PRODUTOR: 'Produtor',
  VAREJISTA: 'Varejista',
  ADMIN: 'Administrador',
};

const BANNER_IMAGE = '/Hero_image.jpg';

const userTypeLabel = computed(() => {
  const p = profile.value;
  if (!p) return props.roleLabel;
  return USER_TYPE_LABEL[p.user_type] || props.roleLabel;
});

const cityStateLabel = computed(() => {
  const addr = profile.value?.address;
  if (!addr) return 'Localização não informada';

  const cityState = [addr.city, addr.state].filter(Boolean).join(', ');
  return cityState || 'Localização não informada';
});

const fullAddressLabel = computed(() => {
  const addr = profile.value?.address;
  if (!addr) return null;

  const street = [addr.street, addr.number].filter(Boolean).join(', ') || null;
  const neighborhood = addr.neighborhood || null;
  const cityState = [addr.city, addr.state].filter(Boolean).join(' / ') || null;
  const postalCode = formatPostalCode(addr.postal_code);

  const parts = [
    street,
    addr.complement || null,
    [neighborhood, cityState].filter(Boolean).join(' • ') || null,
    postalCode ? `CEP ${postalCode}` : null,
  ];

  return parts.filter(Boolean).join(' — ');
});

const accountSections = computed(() => {
  const p = profile.value;
  if (!p) return [];

  const docType = p.profile?.document_type;
  const docNumber = formatDocument(docType, p.profile?.document_number);

  return [
    {
      title: 'Dados Básicos',
      fields: [
        { label: 'Email', value: p.email },
        { label: 'Tipo de Usuário', value: userTypeLabel.value },
      ],
    },
    {
      title: 'Endereço',
      fields: [{ label: 'Endereço Completo', value: fullAddressLabel.value, full: true }],
    },
    {
      title: 'Informações adicionais',
      fields: [
        {
          label: 'Tipo de Documento',
          value: DOCUMENT_TYPE_LABEL[docType] ?? docType,
        },
        { label: 'Número do Documento', value: docNumber || p.profile?.document_number },
        { label: 'Nome Fantasia', value: p.profile?.trade_name, full: true },
      ],
    },
  ];
});
</script>
