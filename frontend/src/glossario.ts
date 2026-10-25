// Destaque das palavras do glossário ("Palavras sublinhadas têm explicação: toque nelas").
import type { Termo } from './api'

export type Trecho = { texto: string; termo?: Termo }

const escapar = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

export function criarBuscador(termos: Termo[]) {
  const pares = termos.flatMap((t) => t.aliases.map((a) => ({ alias: a, termo: t })))
  pares.sort((a, b) => b.alias.length - a.alias.length)            // "backup em nuvem" antes de "backup"
  if (pares.length === 0) return null
  const re = new RegExp(`(?<![\\p{L}\\p{N}])(${pares.map((p) => escapar(p.alias)).join('|')})(?![\\p{L}\\p{N}])`, 'giu')
  const porAlias = new Map(pares.map((p) => [p.alias.toLocaleLowerCase('pt-BR'), p.termo]))
  return { re, porAlias }
}

/** Divide o texto em trechos; só a primeira ocorrência de cada termo vira destaque, para não poluir a leitura. */
export function segmentar(texto: string, buscador: ReturnType<typeof criarBuscador>, jaUsados = new Set<string>()): Trecho[] {
  if (!buscador) return [{ texto }]
  const saida: Trecho[] = []
  let ultimo = 0
  for (const m of texto.matchAll(buscador.re)) {
    const termo = buscador.porAlias.get(m[0].toLocaleLowerCase('pt-BR'))
    if (!termo || jaUsados.has(termo.id)) continue
    jaUsados.add(termo.id)
    if (m.index! > ultimo) saida.push({ texto: texto.slice(ultimo, m.index) })
    saida.push({ texto: m[0], termo })
    ultimo = m.index! + m[0].length
  }
  if (ultimo < texto.length) saida.push({ texto: texto.slice(ultimo) })
  return saida
}
