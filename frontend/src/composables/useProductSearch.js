import { ref } from 'vue';
import { productSearchService } from '@/services/productSearch';

/**
 * Composable para busca de produtos no serviço externo.
 *
 * Encapsula estado de loading, lista de resultados e tratamento de erros,
 * permitindo reuso em qualquer componente que precise de autocomplete de produtos.
 *
 * @returns {{ options: Ref<Array>, isLoading: Ref<boolean>, search: Function, reset: Function }}
 */
export function useProductSearch() {
  const options = ref([]);
  const isLoading = ref(false);

  async function search(query = '') {
    isLoading.value = true;
    try {
      options.value = await productSearchService.search(query);
    } catch (err) {
      console.error('[useProductSearch] Falha ao buscar produtos:', err);
      options.value = [];
    } finally {
      isLoading.value = false;
    }
  }

  function reset() {
    options.value = [];
    isLoading.value = false;
  }

  return { options, isLoading, search, reset };
}
