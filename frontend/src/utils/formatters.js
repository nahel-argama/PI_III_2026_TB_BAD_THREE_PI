export function formatDocument(type, number) {
  if (!number) return null;
  const digits = String(number).replace(/\D/g, '');
  
  if (type === 'CPF' && digits.length === 11) {
    return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  }
  
  if (type === 'CNPJ' && digits.length === 14) {
    return digits.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  }
  
  return number;
}

export function formatPostalCode(cep) {
  if (!cep) return null;
  const digits = String(cep).replace(/\D/g, '');
  return digits.length === 8 ? digits.replace(/(\d{5})(\d{3})/, '$1-$2') : cep;
}
