<template>
  <div class="credit-card-form mt-4 rounded-xl border border-slate-200 bg-slate-50 p-5">
    <p class="mb-4 text-sm font-bold text-slate-700">Dados do Cartão</p>

    <!-- Número do cartão -->
    <div class="form-group mb-4">
      <label for="cc-number" class="form-label">Número do cartão</label>
      <input
        id="cc-number"
        v-model="form.number"
        type="text"
        inputmode="numeric"
        maxlength="19"
        placeholder="0000 0000 0000 0000"
        class="form-input"
        :class="{ 'form-input--error': errors.number }"
        :disabled="disabled"
        @input="onNumberInput"
        @blur="validateField('number')"
      />
      <p v-if="errors.number" class="form-error">{{ errors.number }}</p>
    </div>

    <!-- Nome do titular -->
    <div class="form-group mb-4">
      <label for="cc-holder" class="form-label">Nome do titular (como no cartão)</label>
      <input
        id="cc-holder"
        v-model="form.holder_name"
        type="text"
        maxlength="120"
        placeholder="NOME COMPLETO"
        class="form-input"
        :class="{ 'form-input--error': errors.holder_name }"
        :disabled="disabled"
        @input="form.holder_name = form.holder_name.toUpperCase()"
        @blur="validateField('holder_name')"
      />
      <p v-if="errors.holder_name" class="form-error">{{ errors.holder_name }}</p>
    </div>

    <!-- Validade + CVV -->
    <div class="grid grid-cols-3 gap-3">
      <div class="form-group">
        <label for="cc-month" class="form-label">Mês</label>
        <select
          id="cc-month"
          v-model.number="form.expiry_month"
          class="form-input"
          :class="{ 'form-input--error': errors.expiry_month }"
          :disabled="disabled"
          @change="validateField('expiry_month')"
        >
          <option :value="null" disabled>MM</option>
          <option v-for="m in 12" :key="m" :value="m">
            {{ String(m).padStart(2, '0') }}
          </option>
        </select>
        <p v-if="errors.expiry_month" class="form-error">{{ errors.expiry_month }}</p>
      </div>

      <div class="form-group">
        <label for="cc-year" class="form-label">Ano</label>
        <select
          id="cc-year"
          v-model.number="form.expiry_year"
          class="form-input"
          :class="{ 'form-input--error': errors.expiry_year }"
          :disabled="disabled"
          @change="validateField('expiry_year')"
        >
          <option :value="null" disabled>AAAA</option>
          <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
        </select>
        <p v-if="errors.expiry_year" class="form-error">{{ errors.expiry_year }}</p>
      </div>

      <div class="form-group">
        <label for="cc-cvv" class="form-label">CVV</label>
        <input
          id="cc-cvv"
          v-model="form.cvv"
          type="text"
          inputmode="numeric"
          maxlength="4"
          placeholder="000"
          class="form-input"
          :class="{ 'form-input--error': errors.cvv }"
          :disabled="disabled"
          @input="form.cvv = form.cvv.replace(/\D/g, '')"
          @blur="validateField('cvv')"
        />
        <p v-if="errors.cvv" class="form-error">{{ errors.cvv }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from 'vue';

const props = defineProps({
  /**
   * Card data object (v-model:cardData)
   * @type {{ holder_name: string, number: string, expiry_month: number|null, expiry_year: number|null, cvv: string }}
   */
  cardData: {
    type: Object,
    default: () => ({}),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:cardData', 'valid']);

// ─── Estado interno ───────────────────────────────────────────────────────────

const currentYear = new Date().getFullYear();

const yearOptions = Array.from({ length: 21 }, (_, i) => currentYear + i);

const form = reactive({
  number: '',
  holder_name: '',
  expiry_month: null,
  expiry_year: null,
  cvv: '',
});

const errors = reactive({
  number: '',
  holder_name: '',
  expiry_month: '',
  expiry_year: '',
  cvv: '',
});

// ─── Máscara do número do cartão ──────────────────────────────────────────────

function onNumberInput() {
  // Remove tudo que não for dígito
  const digits = form.number.replace(/\D/g, '').slice(0, 16);
  // Formata em grupos de 4
  form.number = digits.replace(/(.{4})/g, '$1 ').trim();
}

// ─── Validação ────────────────────────────────────────────────────────────────

function validateField(field) {
  errors[field] = getFieldError(field);
  emitState();
}

function getFieldError(field) {
  switch (field) {
    case 'number': {
      const digits = form.number.replace(/\s/g, '');
      if (!digits) return 'Número do cartão é obrigatório.';
      if (digits.length < 13 || digits.length > 16) return 'Número deve ter entre 13 e 16 dígitos.';
      return '';
    }
    case 'holder_name': {
      const name = form.holder_name.trim();
      if (!name) return 'Nome do titular é obrigatório.';
      if (!/^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$/.test(name)) return 'Apenas letras são permitidas.';
      if (name.split(/\s+/).filter(Boolean).length < 2) return 'Informe nome e sobrenome.';
      return '';
    }
    case 'expiry_month': {
      if (!form.expiry_month) return 'Mês é obrigatório.';
      return '';
    }
    case 'expiry_year': {
      if (!form.expiry_year) return 'Ano é obrigatório.';
      // Validar expiração combinada
      if (form.expiry_month && form.expiry_year) {
        const expiry = new Date(form.expiry_year, form.expiry_month - 1, 1);
        const now = new Date();
        const firstOfCurrentMonth = new Date(now.getFullYear(), now.getMonth(), 1);
        if (expiry < firstOfCurrentMonth) return 'Cartão expirado.';
      }
      return '';
    }
    case 'cvv': {
      const cvv = form.cvv;
      if (!cvv) return 'CVV é obrigatório.';
      if (!/^\d{3,4}$/.test(cvv)) return 'CVV deve ter 3 ou 4 dígitos.';
      if (cvv === '000') return 'CVV inválido.';
      return '';
    }
    default:
      return '';
  }
}

function validateAll() {
  const fields = ['number', 'holder_name', 'expiry_month', 'expiry_year', 'cvv'];
  fields.forEach((f) => { errors[f] = getFieldError(f); });
}

// ─── Computed: cartão válido ──────────────────────────────────────────────────

const isValid = computed(() => {
  const fields = ['number', 'holder_name', 'expiry_month', 'expiry_year', 'cvv'];
  const hasValues =
    form.number && form.holder_name && form.expiry_month && form.expiry_year && form.cvv;
  if (!hasValues) return false;
  return fields.every((f) => getFieldError(f) === '');
});

// ─── Emissões reativas ────────────────────────────────────────────────────────

function emitState() {
  emit('update:cardData', {
    holder_name: form.holder_name.trim(),
    number: form.number.replace(/\s/g, ''),
    expiry_month: form.expiry_month,
    expiry_year: form.expiry_year,
    cvv: form.cvv,
  });
  emit('valid', isValid.value);
}

// Emite sempre que o form muda (para manter o pai sincronizado)
watch(form, () => {
  emitState();
}, { deep: true });

// Valida tudo quando o componente é desabilitado (ex: processando pagamento)
watch(() => props.disabled, (val) => {
  if (!val) validateAll();
});
</script>

<style scoped>
.form-label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #cbd5e1;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #0f172a;
  background: #ffffff;
  transition: border-color 0.15s;
  outline: none;
  appearance: none;
}

.form-input:focus {
  border-color: #16a34a;
}

.form-input:disabled {
  background: #f1f5f9;
  cursor: not-allowed;
  opacity: 0.7;
}

.form-input--error {
  border-color: #ef4444;
}

.form-error {
  margin-top: 4px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #ef4444;
}
</style>
