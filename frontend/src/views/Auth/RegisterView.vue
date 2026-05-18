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
          <div :class="['h-2 w-8 rounded', currentStep >= 1 ? 'bg-green-600' : 'bg-gray-300']"></div>
          <div :class="['h-2 w-8 rounded', currentStep >= 2 ? 'bg-green-600' : 'bg-gray-300']"></div>
          <div :class="['h-2 w-8 rounded', currentStep >= 3 ? 'bg-green-600' : 'bg-gray-300']"></div>
        </div>
      </div>

      <form @submit.prevent="currentStep < 3 ? nextStep() : handleCadastro()">
        <!-- Step 1: basico -->
        <div v-if="currentStep === 1">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Nome Completo</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            />
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
            <label class="mb-2 block text-sm font-bold text-gray-700">Nome fantasia / Razão social</label>
            <input
              v-model="form.nome_fantasia"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            />
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-bold text-gray-700">Senha</label>
            <input
              v-model="form.password"
              type="password"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            />
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
              :placeholder="form.tipo_documento === 'CPF' ? '000.000.000-00' : '00.000.000/0000-00'"
              :maxlength="form.tipo_documento === 'CPF' ? 14 : 18"
              required
              @input="applyDocumentMask"
              @blur="validateDocumento"
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
              <div v-if="isSearchingCep" class="absolute right-3 top-2">
                <svg class="h-5 w-5 animate-spin text-green-800" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
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
              required
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Número</label>
            <input
              v-model="form.numero"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Bairro</label>
            <input
              v-model="form.bairro"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-bold text-gray-700">Cidade</label>
            <input
              v-model="form.cidade"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              required
            />
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
            class="rounded-lg border px-4 py-2 font-bold text-gray-700 hover:bg-gray-100"
            @click="prevStep"
          >
            Anterior
          </button>
          <button
            type="submit"
            class="bg-primary hover:bg-secondary rounded-lg px-4 py-2 font-bold text-white transition duration-300"
          >
            {{ currentStep < 3 ? 'Próximo' : 'Cadastrar' }}
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
import { useRouter } from 'vue-router';
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
const lastSearchedCep = ref('');

const form = reactive({
  name: '',
  email: '',
  type: 'PRODUCER',
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
  cep: '',
  documento: '',
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
  } catch (error) {
    console.error('Erro ao carregar estados:', error);
  } finally {
    isLoadingStates.value = false;
  }
});

watch(() => form.tipo_documento, () => {
  errors.documento = '';
  form.documento = '';
});

watch(() => form.cep, (newVal) => {
  errors.cep = '';
  const cleanCep = newVal.replace(/\D/g, '');
  if (cleanCep.length !== 8) {
    lastSearchedCep.value = '';
  } else if (cleanCep.length === 8 && !isSearchingCep.value) {
    handleCepBlur();
  }
});

watch(() => form.estado, () => {
  errors.estado = '';
});

const nextStep = () => {
  if (currentStep.value === 2) {
    validateDocumento();
    if (errors.documento) {
      toast.warning('Por favor, verifique os dígitos do documento CPF/CNPJ antes de prosseguir.', 'Documento Inválido');
      return;
    }
  } else if (currentStep.value === 3) {
    validateCep();
    if (errors.cep) {
      toast.warning('O CEP informado está incompleto ou a busca automática falhou. Verifique os dados.', 'CEP Inválido');
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
};

const applyCepMask = (event) => {
  form.cep = maskCEP(event.target.value);
};

const validateCep = () => {
  const cep = form.cep.replace(/\D/g, '');
  if (cep.length !== 8) {
    errors.cep = 'CEP invalido.';
    return false;
  }
  // Se já houver um erro (como "CEP não encontrado"), não limpamos aqui
  // Isso impede o envio se a busca falhou anteriormente
  if (errors.cep) {
    return false;
  }
  return true;
};

const handleCepBlur = async () => {
  const cep = form.cep.replace(/\D/g, '');
  if (cep === lastSearchedCep.value) return;

  const isValid = validateCep();
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
  } catch (error) {
    console.error('Erro ao buscar endereço:', error);
    errors.cep = 'CEP não encontrado ou erro na busca.';
    lastSearchedCep.value = '';
  } finally {
    isSearchingCep.value = false;
  }
};

const validateDocumento = () => {
  const doc = form.documento.replace(/\D/g, '');
  if (form.tipo_documento === 'CPF') {
    if (doc.length !== 11) {
      errors.documento = 'CPF invalido.';
    } else {
      errors.documento = '';
    }
  } else if (form.tipo_documento === 'CNPJ') {
    if (doc.length !== 14) {
      errors.documento = 'CNPJ invalido.';
    } else {
      errors.documento = '';
    }
  }
};

const handleCadastro = async () => {
  // Garantir que a busca do CEP foi feita se o campo estiver preenchido
  if (form.cep.replace(/\D/g, '').length === 8 && !form.rua) {
    await handleCepBlur();
  }

  // Validar campos antes de enviar
  validateCep();
  validateDocumento();

  if (!form.estado) {
    errors.estado = 'Selecione um estado.';
  } else {
    errors.estado = '';
  }

  if (errors.cep || errors.documento || errors.estado) {
    toast.warning('Existem erros pendentes nos campos do formulário. Corrija-os para continuar.', 'Formulário Incompleto');
    return;
  }

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
        number: form.numero || 'S/N',
        complement: '',
        neighborhood: form.bairro,
        city: form.cidade,
        state: form.estado,
        postal_code: form.cep.replace(/\D/g, ''),
      },
    };
    await authStore.signup(signupPayload);

    toast.success('Sua conta foi criada com sucesso! Seja bem-vindo à nossa plataforma.', 'Cadastro Concluído', {
      duration: 5000,
    });
    router.push('/dashboard');
  } catch (error) {
    console.error('Erro no cadastro:', error);
    const backendMessage =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.response?.data?.non_field_errors?.[0] ||
      error?.response?.data ||
      error?.message ||
      'Erro desconhecido';
      
    const errorDetails = typeof backendMessage === 'object' 
      ? JSON.stringify(backendMessage) 
      : String(backendMessage);

    toast.error(`Falha ao concluir seu cadastro. Detalhes: ${errorDetails}`, 'Falha no Cadastro');
  }
};
</script>
