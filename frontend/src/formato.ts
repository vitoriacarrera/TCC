// Formatação em português do Brasil.

const moeda = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 })

export function reais(v: number): string {
  return moeda.format(Math.round(v))
}

/** "R$ 1,2 milhão", "R$ 97 mil": para títulos e resumos. Abaixo de mil, valor exato. */
export function reaisCurto(v: number): string {
  const a = Math.abs(v)
  const fmt = (x: number) => x.toLocaleString('pt-BR', { maximumFractionDigits: x < 10 ? 1 : 0 })
  if (a >= 1e6) {
    const m = v / 1e6
    return `R$ ${fmt(m)} ${Math.abs(m) < 2 ? 'milhão' : 'milhões'}`
  }
  if (a >= 1e3) return `R$ ${fmt(v / 1e3)} mil`
  return reais(v)
}

/** 0,043 → "4,3%"; 0,43 → "43%". */
export function pct(v: number): string {
  const p = v * 100
  const casas = p > 0 && p < 10 ? 1 : 0
  return `${p.toLocaleString('pt-BR', { minimumFractionDigits: casas, maximumFractionDigits: casas })}%`
}

/** Lê "1.200.000", "1200000,50" ou "R$ 1.200.000" como número; null se vazio ou inválido. */
export function lerMoeda(texto: string): number | null {
  const limpo = texto.replace(/[^\d,]/g, '').replace(',', '.')
  if (!limpo) return null
  const n = Number(limpo)
  return Number.isFinite(n) ? n : null
}

export function digitarMoeda(texto: string): string {
  const n = lerMoeda(texto)
  return n === null ? '' : Math.round(n).toLocaleString('pt-BR')
}
