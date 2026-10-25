// Estado da jornada. Fica só nesta aba do navegador (sessionStorage): some ao fechar a aba e nunca vai ao servidor
// sem o gestor pedir a simulação (ADR-005).
import type { Perfil, Questionario, Respostas, Simulacao } from './api'
import { lerMoeda } from './formato'

export type Etapa = 'inicio' | 'empresa' | 'financeiro' | 'ativos' | 'questionario' | 'resultado'

export type Estado = {
  etapa: Etapa
  setor: string | null
  receitaTexto: string
  usuariosTexto: string
  custoHoraTexto: string
  custoHoraNaoSei: boolean
  apetite: string | null
  tolerancia: string | null
  ativo_critico: string | null
  tipo_dado: string | null
  registros_pessoais: string | null
  questionario: Questionario | null
  respostas: Respostas
  grupo: number
  simulacao: Simulacao | null
  contribuiu: boolean
}

export const INICIAL: Estado = {
  etapa: 'inicio', setor: null, receitaTexto: '', usuariosTexto: '', custoHoraTexto: '', custoHoraNaoSei: false,
  apetite: null, tolerancia: null, ativo_critico: null, tipo_dado: null, registros_pessoais: null,
  questionario: null, respostas: {}, grupo: 0, simulacao: null, contribuiu: false,
}

const CHAVE = 'ciberdecide:sessao'

export function carregar(): Estado {
  try {
    const t = sessionStorage.getItem(CHAVE)
    return t ? { ...INICIAL, ...(JSON.parse(t) as Partial<Estado>) } : INICIAL
  } catch {
    return INICIAL
  }
}

export function salvar(e: Estado): void {
  try { sessionStorage.setItem(CHAVE, JSON.stringify(e)) } catch { /* navegação privada: segue só em memória */ }
}

export function apagar(): void {
  try { sessionStorage.removeItem(CHAVE) } catch { /* nada a apagar */ }
}

export function receita(e: Estado): number | null {
  return lerMoeda(e.receitaTexto)
}

export function usuarios(e: Estado): number | null {
  const n = Number(e.usuariosTexto.replace(/\D/g, ''))
  return Number.isInteger(n) && n >= 1 ? n : null
}

export function montarPerfil(e: Estado): Perfil | null {
  const r = receita(e)
  const u = usuarios(e)
  const custo = e.custoHoraNaoSei ? null : lerMoeda(e.custoHoraTexto)
  if (!e.setor || !r || !u || !e.apetite || !e.tolerancia || !e.ativo_critico || !e.tipo_dado || !e.registros_pessoais) return null
  if (!e.custoHoraNaoSei && !custo) return null
  return {
    setor: e.setor, receita_operacional_bruta: r, usuarios_ti: u, registros_pessoais: e.registros_pessoais,
    tipo_dado: e.tipo_dado, ativo_critico: e.ativo_critico, apetite: e.apetite, tolerancia: e.tolerancia,
    custo_hora_parada: custo,
  }
}
