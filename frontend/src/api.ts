// Cliente da API (backend/src/riskpme/api). Tipos espelham as respostas das rotas.

// Sem VITE_API_URL, usa /api, que o Vite repassa para a API local (vite.config.ts).
const BASE = ((import.meta.env.VITE_API_URL as string | undefined) || '/api').replace(/\/$/, '')

export type Opcao = { id: string; rotulo: string; valor?: number; selo?: string; valor_por_setor?: boolean }
export type PerguntaContexto = {
  id: string
  texto: string
  ajuda: string
  tipo: string
  opcoes?: Opcao[]
  como_calcular?: string
  onde_encontrar?: string
  mensagem_porte?: string
  mensagem_padrao?: string
}
export type Termo = { id: string; termo: string; aliases: string[]; explicacao: string; exemplo?: string | null }
export type Conceito = { id: string; termo: string; explicacao: string }
export type NivelMatriz = { nivel: number; id: string; rotulo: string; maximo?: number }
export type Catalogo = {
  versao: string
  instrucoes: { titulo: string; texto: string; tempo_estimado_min: Record<string, number> }
  aviso_legal: string
  escala: { valor: number | null; rotulo: string }[]
  funcoes: Record<string, { nome: string; descricao: string }>
  setores: { id: string; nome: string; exemplos: string }[]
  portes: { nivel: number; nome: string; rob_min: number; rob_max: number }[]
  contexto: { financeiro: PerguntaContexto[]; ativos: PerguntaContexto[]; calibracao_risco: PerguntaContexto[] }
  matriz: {
    horizonte_anos: number
    impacto: NivelMatriz[]
    probabilidade: NivelMatriz[]
    cores: { cor: 'verde' | 'amarelo' | 'vermelho'; soma: number[]; significado: string }[]
    selo_ruptura: { texto: string; transferencia: string; texto_preparacao: string }
  }
  cenarios: { id: string; nome: string; descricao: string }[]
  glossario: { termos: Termo[]; conceitos: Conceito[] }
}

export type PerguntaQuestionario = { id: string; funcao: string; texto: string; respostas: string[]; ajuda: string }
export type Questionario = {
  porte: { nivel: number; nome: string }
  mensagem_porte: string
  tempo_estimado_min: number | null
  perguntas: PerguntaQuestionario[]
}

export type Perfil = {
  setor: string
  receita_operacional_bruta: number
  usuarios_ti: number
  registros_pessoais: string
  tipo_dado: string
  ativo_critico: string
  apetite: string
  tolerancia: string
  custo_hora_parada: number | null
}
export type Respostas = Record<string, number | null>

export type ResultadoCenario = {
  id: string
  nome: string
  maturidade: number
  maturidade_resposta: number
  vulnerabilidade: number
  fator_primaria: number
  fator_secundaria: number
  lef: number
  chance_ano: number
  chance_horizonte: number
  perda_esperada: number
  p90_quando_ocorre: number
  nivel_impacto: number
  nivel_probabilidade: number
  cor: 'verde' | 'amarelo' | 'vermelho'
  ruptura: boolean
  destaque: boolean
}
export type Acao = {
  prioridade: number
  controle: string
  controle_nome: string
  titulo: string
  perguntas: string[]
  recomendacoes: string[]
  reducao_perda_anual: number
  reducao_periodo_ruim: number
  custo_anual: number
  rosi: number | null
  acima_do_limite: boolean
  selo: string | null
  protege_ruptura: string[]
  impacto_ruptura: Record<string, number>
}
export type Ruptura = {
  cenario: string
  texto: string
  transferencia: string
  texto_preparacao: string
  preparacao: string[]
  impacto_atual: number
  impacto_com_preparacao: number
  tolerancia: number
  sai_da_ruptura: boolean
}
export type Simulacao = {
  porte: { nivel: number; nome: string }
  resultado: {
    iteracoes: number
    apetite_rs: number
    tolerancia_rs: number
    custo_hora_parada: number
    custo_hora_estimado: boolean
    horizonte_anos: number
    cenarios: ResultadoCenario[]
    chance_algum_prejuizo: number
    chance_algum_prejuizo_horizonte: number
    perda_esperada_total: number
    percentis_total: Record<string, number>
    nao_sei: string[]
  }
  matriz: { celulas: Record<string, string[]> }
  plano: {
    perda_esperada_atual: number
    limite_investimento: number
    horizonte_anos: number
    perda_periodo_ruim_atual: number
    acoes: Acao[]
    ruptura: Ruptura[]
  }
  versao_catalogo: string
  resumo_pesquisa: Record<string, unknown>
  comprovante_contribuicao: string
}

export class ErroApi extends Error {
  status: number
  constructor(status: number, mensagem: string) {
    super(mensagem)
    this.status = status
  }
}

function mensagemDeErro(status: number, corpo: unknown): string {
  if (status === 429) return 'Muitas tentativas seguidas. Aguarde um minuto e tente de novo.'
  const d = (corpo as { detail?: unknown })?.detail
  if (typeof d === 'string') return d
  if (Array.isArray(d)) return 'Algum campo ficou com um valor que não conseguimos usar. Confira as respostas.'
  if (status === 502 || status === 503 || status === 504) return 'O servidor de cálculo não respondeu. Confira se a API está rodando e tente de novo.'
  return 'Não foi possível falar com o servidor. Tente de novo em instantes.'
}

async function chamar<T>(caminho: string, corpo?: unknown): Promise<T> {
  let r: Response
  try {
    r = await fetch(BASE + caminho, corpo === undefined ? { method: 'GET' } : {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    })
  } catch {
    throw new ErroApi(0, 'Não foi possível falar com o servidor. Confira sua conexão e tente de novo.')
  }
  const dados = await r.json().catch(() => null)
  if (!r.ok) throw new ErroApi(r.status, mensagemDeErro(r.status, dados))
  return dados as T
}

export const api = {
  catalogo: () => chamar<Catalogo>('/catalogo'),
  questionario: (setor: string, receita: number, usuarios: number) =>
    chamar<Questionario>('/questionario', { setor, receita_operacional_bruta: receita, usuarios_ti: usuarios }),
  simular: (perfil: Perfil, respostas: Respostas) => chamar<Simulacao>('/simulacoes', { perfil, respostas }),
  contribuir: (setor: string, porte: number, respostas: Respostas, comprovante: string, resultado: Record<string, unknown>) =>
    chamar<{ gravado: boolean }>('/contribuicoes', { consentimento: true, setor, porte, respostas, comprovante, resultado }),
}
