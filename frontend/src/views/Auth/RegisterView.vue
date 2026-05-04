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
              <option value="PRODUTOR">Produtor</option>
              <option value="VAREJISTA">Varejista</option>
            </select>
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
              v-model="form.documento"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              :placeholder="form.tipo_documento === 'CPF' ? '000.000.000-00' : '00.000.000/0000-00'"
              required
              @blur="validateDocumento"
            />
            <p v-if="errors.documento" class="mt-1 text-sm text-red-600">{{ errors.documento }}</p>
          </div>

          <div v-if="form.type === 'PRODUTOR'" class="mb-6">
            <label class="mb-2 block text-sm font-bold text-gray-700">Nome de usuário (Opcional)</label>
            <input
              v-model="form.nome_fantasia"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
            />
          </div>
        </div>

        <!-- Step 3: endereços -->
        <div v-if="currentStep === 3">
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
            <label class="mb-2 block text-sm font-bold text-gray-700">Estado</label>
            <input
              v-model="form.estado"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              placeholder="Ex: SP"
              maxlength="2"
              required
            />
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-bold text-gray-700">CEP</label>
            <input
              v-model="form.cep"
              type="text"
              class="w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-green-800 focus:outline-none"
              placeholder="00000-000"
              required
              @blur="validateCep"
            />
            <p v-if="errors.cep" class="mt-1 text-sm text-red-600">{{ errors.cep }}</p>
          </div>
        </div>

        <div class="flex justify-between">
          <button
            v-if="currentStep > 1"
            type="button"
            @click="prevStep"
            class="rounded-lg border px-4 py-2 font-bold text-gray-700 hover:bg-gray-100"
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
import { reactive, ref, watch } from 'vue';
import api from '../../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();
const currentStep = ref(1);

const form = reactive({
  name: '',
  email: '',
  type: 'PRODUTOR',
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
});

watch(() => form.tipo_documento, () => {
  errors.documento = '';
  form.documento = '';
});

const nextStep = () => {
  if (currentStep.value === 2) {
    validateDocumento();
    if (errors.documento) {
      alert('Corrija o documento antes de prosseguir.');
      return;
    }
  } else if (currentStep.value === 3) {
    validateCep();
    if (errors.cep) {
      alert('Corrija o CEP antes de prosseguir.');
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

const validateCep = () => {
  const cep = form.cep.replace(/\D/g, '');
  if (cep.length !== 8) {
    errors.cep = 'CEP invalido.';
  } else {
    errors.cep = '';
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
  // Validar campos antes de enviar
  validateCep();
  validateDocumento();
  if (errors.cep || errors.documento) {
    alert('Corrija os erros nos campos antes de cadastrar.');
    return;
  }

  try {
    const userPayload = {
      name: form.name,
      email: form.email,
      type: form.type,
      password: form.password,
    };
    await api.post('/users/', userPayload);

    const loginResponse = await api.post('/users/login/', {
      email: form.email,
      password: form.password,
    });
    const token = loginResponse.data.access;
    if (!token) {
      throw new Error('Token não recebido após login.');
    }
    localStorage.setItem('token', token);

    const profilePayload = {
      tipo_documento: form.tipo_documento,
      documento: form.documento,
    };
    if (form.type === 'PRODUTOR') {
      profilePayload.nome_fantasia = form.nome_fantasia;
      await api.post('/produtor/', profilePayload);
    } else {
      await api.post('/varejista/', profilePayload);
    }

    const addressPayload = {
      rua: form.rua,
      numero: form.numero,
      bairro: form.bairro,
      cidade: form.cidade,
      estado: form.estado,
      cep: form.cep,
    };
    await api.post('/endereco/', addressPayload);

    alert('Cadastro realizado com sucesso!');
    router.push('/login');
  } catch (error) {
    console.error('Erro no cadastro:', error);
    const backendMessage = error?.response?.data || error?.message || 'Erro desconhecido';
    alert(`Falha ao cadastrar. Detalhes: ${JSON.stringify(backendMessage)}`);
  }
};
</script>
