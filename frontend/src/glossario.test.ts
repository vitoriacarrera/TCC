import { describe, expect, it } from 'vitest'
import { criarBuscador, segmentar } from './glossario'
import { lerMoeda, pct, reaisCurto } from './formato'

const termos = [
  { id: 'backup', termo: 'Backup', aliases: ['backup', 'cópia de segurança'], explicacao: 'Cópia dos arquivos.' },
  { id: 'nuvem', termo: 'Backup em nuvem', aliases: ['backup em nuvem'], explicacao: 'Cópia guardada na internet.' },
]

describe('glossário', () => {
  const b = criarBuscador(termos)
  it('prefere o termo mais longo e destaca só a primeira vez', () => {
    const t = segmentar('Faça backup em nuvem e teste o Backup todo mês.', b)
    expect(t.filter((x) => x.termo).map((x) => x.termo!.id)).toEqual(['nuvem', 'backup'])
    expect(t.map((x) => x.texto).join('')).toBe('Faça backup em nuvem e teste o Backup todo mês.')
  })
  it('não destaca pedaço de palavra', () => {
    expect(segmentar('backupzinho', b).some((x) => x.termo)).toBe(false)
  })
  it('respeita acentos', () => {
    expect(segmentar('Tenha uma cópia de segurança.', b).find((x) => x.termo)?.termo?.id).toBe('backup')
  })
})

describe('formato', () => {
  it('lê moeda brasileira', () => {
    expect(lerMoeda('R$ 1.200.000')).toBe(1200000)
    expect(lerMoeda('1.500,50')).toBe(1500.5)
    expect(lerMoeda('')).toBeNull()
  })
  it('resume valores e porcentagens', () => {
    expect(reaisCurto(97324)).toBe('R$ 97 mil')
    expect(reaisCurto(1_200_000)).toBe('R$ 1,2 milhão')
    expect(pct(0.043)).toBe('4,3%')
    expect(pct(0.43)).toBe('43%')
  })
})
