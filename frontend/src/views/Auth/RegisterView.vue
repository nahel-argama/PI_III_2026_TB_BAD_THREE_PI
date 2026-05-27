<template>
  <div class="relative flex min-h-screen items-center justify-center bg-gray-100">
    <RouterLink
      to="/"
      class="absolute top-4 left-4 flex items-center gap-2 rounded-md bg-white/80 px-3 py-2 text-sm font-medium text-slate-700 shadow-md backdrop-blur hover:bg-white"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-4 w-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Voltar
    </RouterLink>

    <div class="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Criar Conta</h2>

      <div class="mb-6 flex justify-center">
        <div class="flex space-x-2">
          <div
            :class="['h-2 w-8 rounded', currentStep >= 1 ? 'bg-green-600' : 'bg-gray-300']"
          ></div>
          <div
            :class="['h-2 w-8 rounded', currentStep >= 2 ? 'bg-green-600' : 'bg-gray-300']"
          ></div>
          <div
            :class="['h-2 w-8 rounded', currentStep >= 3 ? 'bg-green-600' : 'bg-gray-300']"
          ></div>
        </div>
      </div>

      <form novalidate @submit.prevent="currentStep < 3 ? nextStep() : handleCadastro()">
        <!-- Step 1: basico -->
        <div v-if="currentStep === 1">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Nome Completo</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.name }"
              required
              @input="errors.name && validateName()"
            />
            <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.email }"
              required
              @input="errors.email && validateEmail()"
            />
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Eu sou um:</label>
            <select
              v-model="form.type"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            >
              <option value="PRODUCER">Produtor</option>
              <option value="RETAILER">Varejista</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700"
              >Nome fantasia / Razão social</label
            >
            <input
              v-model="form.nome_fantasia"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.nome_fantasia }"
              required
              @input="errors.nome_fantasia && validateNomeFantasia()"
            />
            <p v-if="errors.nome_fantasia" class="mt-1 text-sm text-red-600">
              {{ errors.nome_fantasia }}
            </p>
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-bold text-gray-700">Senha</label>
            <input
              v-model="form.password"
              type="password"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.password }"
              required
              @input="errors.password && validatePassword()"
            />
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
          </div>
        </div>

        <!-- Step 2: documentos -->
        <div v-if="currentStep === 2">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Tipo de Documento</label>
            <select
              v-model="form.tipo_documento"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            >
              <option value="CPF">CPF</option>
              <option value="CNPJ">CNPJ</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Documento</label>
            <input
              :value="form.documento"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.documento }"
              :placeholder="form.tipo_documento === 'CPF' ? '000.000.000-00' : '00.000.000/0000-00'"
              :maxlength="form.tipo_documento === 'CPF' ? 14 : 18"
              required
              @input="applyDocumentMask"
            />
            <p v-if="errors.documento" class="mt-1 text-sm text-red-600">{{ errors.documento }}</p>
          </div>
        </div>

        <!-- Step 3: endereços -->
        <div v-if="currentStep === 3">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">CEP</label>
            <div class="relative">
              <input
                :value="form.cep"
                type="text"
                class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
                :class="{ 'border-red-500': errors.cep, 'bg-gray-50': isSearchingCep }"
                placeholder="00000-000"
                maxlength="9"
                required
                :disabled="isSearchingCep"
                @input="applyCepMask"
                @blur="handleCepBlur"
              />
              <div v-if="isSearchingCep" class="absolute top-2 right-3">
                <svg
                  class="h-5 w-5 animate-spin text-green-800"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              </div>
            </div>
            <p v-if="errors.cep" class="mt-1 text-sm text-red-600">{{ errors.cep }}</p>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Rua</label>
            <input
              v-model="form.rua"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.rua }"
              required
              @input="errors.rua && validateRua()"
            />
            <p v-if="errors.rua" class="mt-1 text-sm text-red-600">{{ errors.rua }}</p>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Número</label>
            <input
              v-model="form.numero"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.numero }"
              required
              @input="errors.numero && validateNumero()"
            />
            <p v-if="errors.numero" class="mt-1 text-sm text-red-600">{{ errors.numero }}</p>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Bairro</label>
            <input
              v-model="form.bairro"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.bairro }"
              required
              @input="errors.bairro && validateBairro()"
            />
            <p v-if="errors.bairro" class="mt-1 text-sm text-red-600">{{ errors.bairro }}</p>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Cidade</label>
            <input
              v-model="form.cidade"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :class="{ 'border-red-500': errors.cidade }"
              required
              @input="errors.cidade && validateCidade()"
            />
            <p v-if="errors.cidade" class="mt-1 text-sm text-red-600">{{ errors.cidade }}</p>
          </div>

          <div class="mb-4">
            <AppSelect
              v-model="form.estado"
              :options="stateOptions"
              :loading="isLoadingStates"
              label="Estado"
              placeholder="Selecione o estado"
              required
              :error="errors.estado"
            />
          </div>
        </div>

        <div class="flex justify-between">
          <button
            v-if="currentStep > 1"
            type="button"
            class="rounded-lg border px-4 py-2 font-bold text-gray-700 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-70"
            :disabled="isLoading"
            @click="prevStep"
          >
            Anterior
          </button>
          <button
            type="submit"
            class="bg-primary hover:bg-secondary flex items-center justify-center rounded-lg px-4 py-2 font-bold text-white transition duration-300 disabled:cursor-not-allowed disabled:opacity-70"
            :disabled="isLoading"
          >
            <svg
              v-if="isLoading && currentStep === 3"
              class="mr-2 h-5 w-5 animate-spin text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span v-if="currentStep < 3">Próximo</span>
            <span v-else>{{ isLoading ? 'Cadastrando...' : 'Cadastrar' }}</span>
          </button>
        </div>
      </form>

      <RouterLink to="/login" class="mt-6 block text-center text-blue-800">
        Já tem uma conta?
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { fetchAddressByCep, fetchStates } from '@/services/brasilApi';
import AppSelect from '@/components/ui/AppSelect.vue';
import { useToast } from '@/composables/useToast';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();
const currentStep = ref(1);
const isSearchingCep = ref(false);
const isLoadingStates = ref(false);
const isLoading = ref(false);
const lastSearchedCep = ref('');

const route = useRoute();

const initialType = ['PRODUCER', 'RETAILER'].includes(route.query.type)
  ? route.query.type
  : 'PRODUCER';

const form = reactive({
  name: '',
  email: '',
  type: initialType,
  password: '',
  tipo_documento: 'CPF',
  documento: '',
  nome_fantasia: '',
  rua: '',
  numero: '',
  bairro: '',
  cidade: '',
  estado: '',
  cep: '',
});

const errors = reactive({
  name: '',
  email: '',
  nome_fantasia: '',
  password: '',
  documento: '',
  cep: '',
  rua: '',
  numero: '',
  bairro: '',
  cidade: '',
  estado: '',
});

const stateOptions = ref([]);

onMounted(async () => {
  isLoadingStates.value = true;
  try {
    const data = await fetchStates();
    stateOptions.value = data
      .map((s) => ({
        label: `${s.nome} (${s.sigla})`,
        value: s.sigla,
      }))
      .sort((a, b) => a.label.localeCompare(b.label));
  } catch {
    // Silencia falha ao carregar estados
  } finally {
    isLoadingStates.value = false;
  }
});

watch(
  () => form.tipo_documento,
  () => {
    errors.documento = '';
    form.documento = '';
  },
);

watch(
  () => form.cep,
  (newVal) => {
    errors.cep = '';
    const cleanCep = newVal.replace(/\D/g, '');
    if (cleanCep.length !== 8) {
      lastSearchedCep.value = '';
    } else if (cleanCep.length === 8 && !isSearchingCep.value) {
      handleCepBlur();
    }
  },
);

watch(
  () => form.estado,
  () => {
    errors.estado = '';
  },
);

const nextStep = async () => {
  if (currentStep.value === 1) {
    if (!validateName()) {
      toast.warning('O campo Nome Completo é obrigatório.', 'Nome Completo Inválido');
      return;
    }
    if (!validateEmail()) {
      toast.warning(errors.email, 'Email Inválido');
      return;
    }

    // Verificar se o email já existe no backend
    try {
      const emailCheck = await authStore.checkEmail(form.email);
      if (emailCheck.exists) {
        errors.email = 'Este e-mail já está cadastrado.';
        toast.warning(errors.email, 'Email já cadastrado');
        return;
      }
    } catch {
      toast.error('Erro ao verificar disponibilidade do e-mail.', 'Falha na Verificação');
      return;
    }

    if (!validateNomeFantasia()) {
      toast.warning(
        'O campo Nome fantasia / Razão social é obrigatório.',
        'Nome Fantasia Inválido',
      );
      return;
    }
    if (!validatePassword()) {
      toast.warning(errors.password, 'Senha Inválida');
      return;
    }
  } else if (currentStep.value === 2) {
    if (!validateDocumento()) {
      toast.warning(errors.documento, 'Documento Inválido');
      return;
    }

    // Verificar se o documento já existe no backend
    try {
      const docCheck = await authStore.checkDocument(form.documento);
      if (docCheck.exists) {
        errors.documento = 'Este documento já está cadastrado.';
        toast.warning(errors.documento, 'Documento já cadastrado');
        return;
      }
    } catch {
      toast.error('Erro ao verificar disponibilidade do documento.', 'Falha na Verificação');
      return;
    }
  }
  if (currentStep.value < 3) {
    currentStep.value++;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const maskCPF = (value) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})/, '$1-$2')
    .replace(/(-\d{2})\d+?$/, '$1');
};

const maskCNPJ = (value) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '$1.$2')
    .replace(/(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
    .replace(/\.(\d{3})(\d)/, '.$1/$2')
    .replace(/(\d{4})(\d)/, '$1-$2')
    .replace(/(-\d{2})\d+?$/, '$1');
};

const maskCEP = (value) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{5})(\d)/, '$1-$2')
    .replace(/(-\d{3})\d+?$/, '$1');
};

const applyDocumentMask = (event) => {
  const value = event.target.value;
  if (form.tipo_documento === 'CPF') {
    form.documento = maskCPF(value);
  } else {
    form.documento = maskCNPJ(value);
  }
  if (errors.documento) {
    validateDocumento();
  }
};

const applyCepMask = (event) => {
  form.cep = maskCEP(event.target.value);
};

const validateCep = (showError = true) => {
  const cep = form.cep.replace(/\D/g, '');
  if (!cep) {
    if (showError) errors.cep = 'O CEP é obrigatório.';
    return false;
  }
  if (cep.length !== 8) {
    if (showError) errors.cep = 'CEP inválido.';
    return false;
  }
  if (errors.cep && errors.cep !== 'CEP inválido.' && errors.cep !== 'O CEP é obrigatório.') {
    return false;
  }
  if (showError) errors.cep = '';
  return true;
};

const handleCepBlur = async () => {
  const cep = form.cep.replace(/\D/g, '');
  if (cep === lastSearchedCep.value) return;

  const isValid = validateCep(false);
  if (!isValid) return;

  isSearchingCep.value = true;
  try {
    const data = await fetchAddressByCep(cep);
    form.rua = data.street || '';
    form.bairro = data.neighborhood || '';
    form.cidade = data.city || '';
    form.estado = data.state || '';
    errors.cep = '';
    lastSearchedCep.value = cep;
  } catch {
    errors.cep = 'CEP não encontrado ou erro na busca.';
    lastSearchedCep.value = '';
  } finally {
    isSearchingCep.value = false;
  }
};

const validateDocumento = () => {
  const doc = form.documento.replace(/\D/g, '');
  if (!doc) {
    errors.documento = 'O documento é obrigatório.';
    return false;
  }
  if (form.tipo_documento === 'CPF') {
    if (doc.length !== 11) {
      errors.documento = 'CPF inválido.';
      return false;
    }
  } else if (form.tipo_documento === 'CNPJ') {
    if (doc.length !== 14) {
      errors.documento = 'CNPJ inválido.';
      return false;
    }
  }
  errors.documento = '';
  return true;
};

const validatePassword = () => {
  if (!form.password) {
    errors.password = 'A senha é obrigatória.';
    return false;
  }
  if (form.password.length < 8) {
    errors.password = 'A senha deve ter pelo menos 8 caracteres.';
    return false;
  }
  errors.password = '';
  return true;
};

const validateName = () => {
  if (!form.name || !form.name.trim()) {
    errors.name = 'O nome completo é obrigatório.';
    return false;
  }
  if (/\d/.test(form.name)) {
    errors.name = 'O nome completo não pode conter números.';
    return false;
  }
  errors.name = '';
  return true;
};

const validateEmail = () => {
  if (!form.email || !form.email.trim()) {
    errors.email = 'O e-mail é obrigatório.';
    return false;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.email)) {
    errors.email = 'Insira um e-mail válido.';
    return false;
  }
  errors.email = '';
  return true;
};

const validateNomeFantasia = () => {
  if (!form.nome_fantasia || !form.nome_fantasia.trim()) {
    errors.nome_fantasia = 'O nome fantasia / razão social é obrigatório.';
    return false;
  }
  if (/\d/.test(form.nome_fantasia)) {
    errors.nome_fantasia = 'O nome fantasia não pode conter números.';
    return false;
  }
  errors.nome_fantasia = '';
  return true;
};

const validateRua = () => {
  if (!form.rua || !form.rua.trim()) {
    errors.rua = 'A rua é obrigatória.';
    return false;
  }
  errors.rua = '';
  return true;
};

const validateNumero = () => {
  if (!form.numero || !form.numero.trim()) {
    errors.numero = 'O número é obrigatório.';
    return false;
  }
  if (!/^\d+$/.test(form.numero)) {
    errors.numero = 'O número deve conter apenas algarismos (números).';
    return false;
  }
  errors.numero = '';
  return true;
};

const validateBairro = () => {
  if (!form.bairro || !form.bairro.trim()) {
    errors.bairro = 'O bairro é obrigatório.';
    return false;
  }
  errors.bairro = '';
  return true;
};

const validateCidade = () => {
  if (!form.cidade || !form.cidade.trim()) {
    errors.cidade = 'A cidade é obrigatória.';
    return false;
  }
  errors.cidade = '';
  return true;
};

const validateEstado = () => {
  if (!form.estado) {
    errors.estado = 'Selecione um estado.';
    return false;
  }
  errors.estado = '';
  return true;
};

const handleCadastro = async () => {
  // Garantir que a busca do CEP foi feita se o campo estiver preenchido
  if (form.cep.replace(/\D/g, '').length === 8 && !form.rua) {
    await handleCepBlur();
  }

  // Validar campos antes de enviar em ordem
  if (!validateCep()) {
    toast.warning(errors.cep, 'CEP Inválido');
    return;
  }
  if (!validateRua()) {
    toast.warning(errors.rua, 'Rua Inválida');
    return;
  }
  if (!validateNumero()) {
    toast.warning(errors.numero, 'Número Inválido');
    return;
  }
  if (!validateBairro()) {
    toast.warning(errors.bairro, 'Bairro Inválido');
    return;
  }
  if (!validateCidade()) {
    toast.warning(errors.cidade, 'Cidade Inválida');
    return;
  }
  if (!validateEstado()) {
    toast.warning(errors.estado, 'Estado Inválido');
    return;
  }

  isLoading.value = true;

  try {
    const signupPayload = {
      name: form.name,
      email: form.email,
      password: form.password,
      user_type: form.type,
      profile: {
        document_type: form.tipo_documento,
        document_number: form.documento.replace(/\D/g, ''),
        trade_name: form.nome_fantasia,
      },
      address: {
        street: form.rua,
        number: form.numero,
        complement: '',
        neighborhood: form.bairro,
        city: form.cidade,
        state: form.estado,
        postal_code: form.cep.replace(/\D/g, ''),
      },
    };
    await authStore.signup(signupPayload);

    toast.success(
      'Sua conta foi criada com sucesso! Seja bem-vindo à nossa plataforma.',
      'Cadastro Concluído',
      {
        duration: 5000,
      },
    );
    router.push('/dashboard');
  } catch (error) {
    const backendMessage =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.response?.data?.non_field_errors?.[0] ||
      error?.response?.data ||
      error?.message ||
      'Erro desconhecido';

    const errorDetails =
      typeof backendMessage === 'object' ? JSON.stringify(backendMessage) : String(backendMessage);

    toast.error(`Falha ao concluir seu cadastro. Detalhes: ${errorDetails}`, 'Falha no Cadastro');
  } finally {
    isLoading.value = false;
  }
};
</script>
