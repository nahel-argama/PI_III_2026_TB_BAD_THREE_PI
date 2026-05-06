import {
  BanknotesIcon,
  BellAlertIcon,
  ChartBarIcon,
  ClipboardDocumentCheckIcon,
  ClipboardDocumentListIcon,
  ClockIcon,
  Cog6ToothIcon,
  MapPinIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  Squares2X2Icon,
  TruckIcon,
  UsersIcon,
} from '@heroicons/vue/24/outline';

export const dashboardProfiles = {
  PRODUTOR: {
    title: 'Painel do Produtor',
    subtitle: 'Acompanhe estoque, oportunidades e preços sugeridos para vender melhor.',
    accent: 'from-emerald-500 via-green-500 to-lime-500',
    headline: 'Seu estoque vira oportunidade com mais clareza.',
    description:
      'Veja os produtos com maior giro, os pedidos em destaque e os alertas de reposição em uma visão simples e rápida.',
    primaryAction: 'Cadastrar Produto',
    secondaryAction: 'Atualizar Estoque',
    navItems: [
      { label: 'Resumo', href: '#resumo', icon: Squares2X2Icon },
      { label: 'Estoque', href: '#estoque', icon: ClipboardDocumentListIcon },
      { label: 'Pedidos', href: '#pedidos', icon: TruckIcon },
      { label: 'Insights', href: '#insights', icon: ChartBarIcon },
      { label: 'Configurações', href: '#configuracoes', icon: Cog6ToothIcon },
    ],
    metrics: [
      {
        label: 'Produtos ativos',
        value: '24',
        helper: '+4 desde ontem',
        tone: 'success',
        icon: ClipboardDocumentCheckIcon,
      },
      {
        label: 'Pedidos em análise',
        value: '08',
        helper: '3 com prioridade alta',
        tone: 'warning',
        icon: ClockIcon,
      },
      {
        label: 'Receita estimada',
        value: 'R$ 18,4 mil',
        helper: 'Com base no estoque atual',
        tone: 'primary',
        icon: BanknotesIcon,
      },
      {
        label: 'Alertas de estoque',
        value: '05',
        helper: 'Itens pedindo reposição',
        tone: 'danger',
        icon: BellAlertIcon,
      },
    ],
    highlights: [
      {
        title: 'Produtor com melhor saída',
        value: 'Tomate orgânico',
        detail: 'Alta procura em varejistas próximos e margem estável.',
      },
      {
        title: 'Preço sugerido',
        value: 'R$ 4,80 / kg',
        detail: 'Faixa de competitividade saudável sem guerra de preço.',
      },
      {
        title: 'Oportunidade geográfica',
        value: '2 varejistas a 12 km',
        detail: 'Potencial de fechamento com logística leve.',
      },
    ],
    activityTitle: 'Demandas relevantes para sua produção',
    activities: [
      {
        title: 'Varejo Central pediu 45 kg de alface',
        detail: 'Entrega prevista em 4 dias. Produto com giro rápido.',
        tag: 'Alta prioridade',
      },
      {
        title: 'Mercado Bom Preço adicionou tomates ao desejo',
        detail: 'Pedido recorrente para reposição semanal.',
        tag: 'Nova chance',
      },
      {
        title: 'Seu estoque de cenoura caiu para 18%',
        detail: 'Sinalizado para reabastecimento e atualização de produção.',
        tag: 'Alerta',
      },
    ],
    quickActions: [
      {
        title: 'Revisar catálogo',
        detail: 'Atualize preço, fotos e disponibilidade.',
        action: 'Abrir catálogo',
        icon: Squares2X2Icon,
      },
      {
        title: 'Ver recomendações',
        detail: 'Consulte oportunidades próximas ao seu município.',
        action: 'Explorar matches',
        icon: MapPinIcon,
      },
    ],
  },
  VAREJISTA: {
    title: 'Painel do Varejo',
    subtitle: 'Monte listas de desejo, encontre fornecedores e acompanhe compras com facilidade.',
    accent: 'from-sky-500 via-cyan-500 to-emerald-500',
    headline: 'Sua reposição fica mais previsível e estratégica.',
    description:
      'Visualize demandas, fornecedores mais próximos e itens que precisam entrar no carrinho com prioridade.',
    primaryAction: 'Nova Lista',
    secondaryAction: 'Buscar Fornecedores',
    navItems: [
      { label: 'Resumo', href: '#resumo', icon: Squares2X2Icon },
      { label: 'Desejos', href: '#desejos', icon: ClipboardDocumentListIcon },
      { label: 'Fornecedores', href: '#fornecedores', icon: UsersIcon },
      { label: 'Economia', href: '#economia', icon: ChartBarIcon },
      { label: 'Configurações', href: '#configuracoes', icon: Cog6ToothIcon },
    ],
    metrics: [
      {
        label: 'Listas ativas',
        value: '06',
        helper: '2 vencem nesta semana',
        tone: 'success',
        icon: ClipboardDocumentCheckIcon,
      },
      {
        label: 'Fornecedores próximos',
        value: '13',
        helper: 'Raio de até 20 km',
        tone: 'primary',
        icon: MapPinIcon,
      },
      {
        label: 'Economia potencial',
        value: 'R$ 2,1 mil',
        helper: 'Em comparação com compras avulsas',
        tone: 'warning',
        icon: BanknotesIcon,
      },
      {
        label: 'Pedidos planejados',
        value: '11',
        helper: 'Itens já priorizados',
        tone: 'danger',
        icon: ClockIcon,
      },
    ],
    highlights: [
      {
        title: 'Fornecedor recomendado',
        value: 'Green Valley',
        detail: 'Mais perto do seu CEP e com estoque suficiente.',
      },
      {
        title: 'Demanda prevista',
        value: 'Hortaliças e raízes',
        detail: 'Sinal forte para abastecimento de final de semana.',
      },
      {
        title: 'Melhor janela de compra',
        value: 'Próximos 3 dias',
        detail: 'Evite ruptura e aproveite a faixa de preço atual.',
      },
    ],
    activityTitle: 'Lista de desejos e compras em andamento',
    activities: [
      {
        title: 'Feira do Centro quer 80 kg de cenoura',
        detail: 'Necessidade prevista para sexta-feira, com entrega programada.',
        tag: 'Nova lista',
      },
      {
        title: 'Supplência de folhosas em monitoramento',
        detail: 'Comparando produtores próximos com melhor disponibilidade.',
        tag: 'Em análise',
      },
      {
        title: 'Preço estimado caiu 4% na região',
        detail: 'Momento favorável para fechar pedido sem excesso de custo.',
        tag: 'Boa janela',
      },
    ],
    quickActions: [
      {
        title: 'Criar lista de desejo',
        detail: 'Registre itens, quantidades e datas previstas.',
        action: 'Adicionar itens',
        icon: PlusIcon,
      },
      {
        title: 'Encontrar fornecedores',
        detail: 'Filtre por proximidade, disponibilidade e categoria.',
        action: 'Abrir busca',
        icon: MagnifyingGlassIcon,
      },
    ],
  },
};

export const dashboardShared = {
  subtitle: 'Protótipo visual em front-end, sem integração com o backend nesta etapa.',
  searchPlaceholder: 'Pesquisar produtos, fornecedores ou listas...',
};
