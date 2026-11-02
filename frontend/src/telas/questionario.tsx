import { useEffect, useMemo, useState } from 'react'
import type { Catalogo, PerguntaQuestionario } from '../api'
import { Ajuda, Cartao, Erro, Navegacao, Texto } from '../componentes/base'
import type { Estado } from '../estado'

type Props = {
  cat: Catalogo
  e: Estado
  mudar: (p: Partial<Estado>) => void
  voltar: () => void
  concluir: () => void
  carregando: boolean
  erro: string | null
}

function grupos(cat: Catalogo, perguntas: PerguntaQuestionario[]) {
  return Object.keys(cat.funcoes)
    .map((f) => ({ funcao: f, ...cat.funcoes[f], perguntas: perguntas.filter((p) => p.funcao === f) }))
    .filter((g) => g.perguntas.length > 0)
}

export function Questionario({ cat, e, mudar, voltar, concluir, carregando, erro }: Props) {
  const lista = useMemo(() => grupos(cat, e.questionario?.perguntas ?? []), [cat, e.questionario])
  const g = lista[Math.min(e.grupo, lista.length - 1)]
  const [avisouEm, setAvisouEm] = useState<number | null>(null)
  const avisou = avisouEm === e.grupo
  useEffect(() => { window.scrollTo({ top: 0 }) }, [e.grupo])
  if (!g) return null

  const inicio = lista.slice(0, e.grupo).reduce((n, x) => n + x.perguntas.length, 0)
  const total = lista.reduce((n, x) => n + x.perguntas.length, 0)
  const respondidas = Object.keys(e.respostas).length
  const faltam = g.perguntas.filter((p) => !(p.id in e.respostas))
  const ultimo = e.grupo >= lista.length - 1

  function avancar() {
    if (faltam.length && !avisou) return setAvisouEm(e.grupo)
    if (ultimo) return concluir()
    mudar({ grupo: e.grupo + 1 })
  }

  return (
    <>
      <div className="mb-5 flex items-baseline justify-between gap-4">
        <p className="text-sm uppercase tracking-[0.14em] text-dourado">Parte {e.grupo + 1} de {lista.length}</p>
        <p className="text-sm text-suave">{respondidas} de {total} respondidas</p>
      </div>
      <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-linha">
        <div className="h-full bg-acao transition-all" style={{ width: `${(respondidas / total) * 100}%` }} />
      </div>
      {e.grupo === 0 && (
        <Cartao className="mb-5 bg-marfim">
          <h2 className="text-xl">{cat.instrucoes.titulo}</h2>
          <p className="mt-2 text-[15px] text-suave">{cat.instrucoes.texto}</p>
        </Cartao>
      )}
      <Cartao>
        <h2 className="text-2xl sm:text-3xl">{g.nome}</h2>
        <p className="mt-1 text-suave">{g.descricao}</p>
        <ol className="mt-8 space-y-10">
          {g.perguntas.map((p, i) => (
            <li key={p.id} id={`q-${p.id}`}>
              <h3 className="font-sans text-lg font-semibold leading-snug text-texto">
                <span className="mr-2 text-dourado">{inicio + i + 1}.</span><Texto>{p.texto}</Texto>
              </h3>
              <Ajuda><Texto>{p.ajuda}</Texto></Ajuda>
              <Escala cat={cat} rotulos={p.respostas} nome={p.id} valor={p.id in e.respostas ? e.respostas[p.id] : undefined}
                marcarFalta={avisou && !(p.id in e.respostas)}
                aoEscolher={(v) => mudar({ respostas: { ...e.respostas, [p.id]: v }, simulacao: null })} />
            </li>
          ))}
        </ol>
        {avisou && faltam.length > 0 && (
          <p role="alert" className="mt-8 rounded-md border-l-4 border-risco-amarelo bg-risco-amarelo/10 px-4 py-3 text-[15px]">
            {faltam.length === 1 ? 'Uma pergunta ficou' : `${faltam.length} perguntas ficaram`} sem resposta. Se continuar,
            {faltam.length === 1 ? ' ela conta' : ' elas contam'} como "Não sei", que é a situação mais cautelosa. Para seguir mesmo assim, toque de novo em continuar.
          </p>
        )}
        <Erro mensagem={erro} />
        <Navegacao voltar={e.grupo === 0 ? voltar : () => mudar({ grupo: e.grupo - 1 })} avancar={avancar}
          rotuloAvancar={ultimo ? 'Ver o resultado' : 'Continuar'} carregando={carregando} />
      </Cartao>
    </>
  )
}

function Escala({ cat, rotulos, nome, valor, aoEscolher, marcarFalta }:
  { cat: Catalogo; rotulos: string[]; nome: string; valor: number | null | undefined; aoEscolher: (v: number | null) => void; marcarFalta: boolean }) {
  return (
    <div role="radiogroup" aria-label="Resposta"
      className={`mt-4 grid gap-2 lg:grid-cols-5 ${marcarFalta ? 'rounded-md ring-2 ring-risco-amarelo ring-offset-4' : ''}`}>
      {cat.escala.map((o) => {
        const sel = valor !== undefined && valor === o.valor
        const naoSei = o.valor === null
        return (
          <label key={String(o.valor)}
            className={`flex cursor-pointer items-center gap-3 rounded-md border px-4 py-3 text-[15px] leading-snug transition
              lg:flex-col lg:items-start lg:gap-2 lg:px-3
              ${naoSei ? 'lg:col-span-5 lg:flex-row lg:items-center lg:justify-center' : ''}
              ${sel ? 'border-acao bg-acao/5 ring-1 ring-acao' : 'border-linha bg-papel hover:border-marinho/40'}`}>
            <input type="radio" name={nome} className="h-4 w-4 accent-[#0e5e57]" checked={sel} onChange={() => aoEscolher(o.valor)} />
            <span>{o.valor === null ? o.rotulo : (rotulos[o.valor] ?? o.rotulo)}</span>
          </label>
        )
      })}
    </div>
  )
}
