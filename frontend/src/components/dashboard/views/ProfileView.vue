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
      <!-- Header com avatar e nome -->
      <ProfileHeader
        :name="profile.name"
        :email="profile.email"
        :user-type="profile.user_type"
        :role-label="roleLabel"
      />

      <!-- Cards de informação -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Dados do perfil -->
        <ProfileInfoCard
          title="Dados da conta"
          :icon="IdentificationIcon"
          :fields="profileFields"
        />

        <!-- Endereço -->
        <ProfileInfoCard
          title="Endereço"
          :icon="MapPinIcon"
          :fields="addressFields"
        />
      </div>
    </template>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import {
  ExclamationTriangleIcon,
  ArrowPathIcon,
  IdentificationIcon,
  MapPinIcon,
} from '@heroicons/vue/24/outline';

import ProfileHeader from './profile/ProfileHeader.vue';
import ProfileInfoCard from './profile/ProfileInfoCard.vue';
import ProfileSkeleton from './profile/ProfileSkeleton.vue';

import { fetchCurrentUserProfile } from '@/services/profile';
import { formatDocument, formatPostalCode } from '@/utils/formatters';

// ── Props ─────────────────────────────────────────────────────────────────────

defineProps({
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



const profileFields = computed(() => {
  const p = profile.value;
  if (!p) return [];

  const docType = p.profile?.document_type;
  const docNumber = formatDocument(docType, p.profile?.document_number);

  return [
    { label: 'Nome', value: p.name },
    { label: 'E-mail', value: p.email, full: false },
    { label: DOCUMENT_TYPE_LABEL[docType] ?? 'Documento', value: docNumber },
    { label: 'Nome fantasia', value: p.profile?.trade_name },
  ];
});

const addressFields = computed(() => {
  const addr = profile.value?.address;
  if (!addr) return [{ label: 'Endereço', value: null, full: true }];

  const street = [addr.street, addr.number].filter(Boolean).join(', ');
  const neighborhood = addr.neighborhood || null;
  const cityState = [addr.city, addr.state].filter(Boolean).join(' - ');
  const postalCode = formatPostalCode(addr.postal_code);

  return [
    { label: 'Logradouro', value: street },
    { label: 'Bairro', value: neighborhood },
    { label: 'Cidade / Estado', value: cityState },
    { label: 'CEP', value: postalCode },
  ];
});
</script>
