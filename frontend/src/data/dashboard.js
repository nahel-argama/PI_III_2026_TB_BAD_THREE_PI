import {
  ArrowPathIcon,
  ArchiveBoxIcon,
  ClipboardDocumentListIcon,
  EyeIcon,
  UserCircleIcon,
} from '@heroicons/vue/24/outline';

export const dashboardProfiles = {
  PRODUTOR: {
    title: 'Painel do Produtor',
    subtitle: 'Acompanhe estoque, oportunidades e preços sugeridos para vender melhor.',
    navItems: [
      { id: 'meu-estoque', label: 'Meu Estoque', icon: ArchiveBoxIcon },
      { id: 'historico-venda', label: 'Histórico de Venda', icon: ArrowPathIcon },
      { id: 'meu-perfil', label: 'Meu Perfil', icon: UserCircleIcon },
    ],
  },
  VAREJISTA: {
    title: 'Painel do Varejo',
    subtitle: 'Monte listas de desejo, encontre fornecedores e acompanhe compras com facilidade.',
    navItems: [
      { id: 'explorar-ofertas', label: 'Explorar Ofertas', icon: EyeIcon },
      { id: 'lista-desejos', label: 'Lista de Desejos', icon: ClipboardDocumentListIcon },
      { id: 'historico-compra', label: 'Histórico de Compra', icon: ArrowPathIcon },
      { id: 'meu-perfil', label: 'Meu Perfil', icon: UserCircleIcon },
    ],
  },
};
