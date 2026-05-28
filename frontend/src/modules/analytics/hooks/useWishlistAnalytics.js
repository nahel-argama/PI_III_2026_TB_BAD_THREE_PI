import { ref, onMounted, watch } from 'vue';
import { wishlistAnalyticsService } from '../services/wishlistAnalytics.service';
import { useToast } from '@/composables/useToast';

export function useWishlistAnalytics() {
  const stateFilter = ref(''); 
  const topFilter = ref(10);
  const userState = ref('');
  
  const data = ref(null);
  const isLoading = ref(false);
  const error = ref(null);
  const toast = useToast();

  const fetchAnalytics = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const params = {
        top: topFilter.value,
      };
      if (stateFilter.value) {
        params.state = stateFilter.value;
      }
      
      const response = await wishlistAnalyticsService.getTopProducts(params);
      data.value = response;

      if (response.user_state) {
        userState.value = response.user_state;
      }
    } catch (err) {
      const is400 = err?.response?.status === 400;
      const detail = err?.response?.data?.detail || err.message;

      if (is400) {
        error.value = detail || 'Verifique os filtros selecionados.';
      } else {
        toast.error('Ocorreu um erro ao carregar analytics. Tente novamente mais tarde.', 'Falha de Conexão');
      }
    } finally {
      isLoading.value = false;
    }
  };

  watch([stateFilter, topFilter], () => {
    fetchAnalytics();
  });

  onMounted(() => {
    fetchAnalytics();
  });

  return {
    stateFilter,
    topFilter,
    data,
    isLoading,
    error,
    userState,
    fetchAnalytics,
  };
}
