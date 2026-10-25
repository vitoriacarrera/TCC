import { createContext, useContext, useEffect, useId, useMemo, useRef, useState, type ReactNode } from 'react'
import type { Termo } from '../api'
import { criarBuscador, segmentar } from '../glossario'
import { MARCA } from '../marca'

// ------------------------------------------------------------------ glossário
const BuscadorCtx = createContext<ReturnType<typeof criarBuscador>>(null)

export function ProvedorGlossario({ termos, children }: { termos: Termo[]; children: ReactNode }) {
  const b = useMemo(() => criarBuscador(termos), [termos])
  return <BuscadorCtx.Provider value={b}>{children}</BuscadorCtx.Provider>
}

/** Texto com as palavras do glossário sublinhadas; tocar abre a explicação. */
export function Texto({ children, className }: { children: string; className?: string }) {
  const b = useContext(BuscadorCtx)
  const trechos = useMemo(() => segmentar(children, b), [children, b])
  return (
    <span className={className}>
      {trechos.map((t, i) => (t.termo ? <TermoDestacado key={i} termo={t.termo} texto={t.texto} /> : <span key={i}>{t.texto}</span>))}
    </span>
  )
}

function TermoDestacado({ termo, texto }: { termo: Termo; texto: string }) {
  const [aberto, setAberto] = useState(false)
  const ref = useRef<HTMLSpanElement>(null)
  const id = useId()
  useEffect(() => {
    if (!aberto) return
    const fora = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setAberto(false) }
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') setAberto(false) }
    document.addEventListener('mousedown', fora)
    document.addEventListener('keydown', esc)
    return () => { document.removeEventListener('mousedown', fora); document.removeEventListener('keydown', esc) }
  }, [aberto])
  return (
    <span ref={ref} className="relative">
      <button type="button" aria-expanded={aberto} aria-controls={id} onClick={() => setAberto((a) => !a)}
        className="cursor-help underline decoration-dourado decoration-dotted decoration-2 underline-offset-4 hover:text-acao">
        {texto}
      </button>
      {aberto && (
        <span id={id} role="note"
          className="fixed inset-x-4 bottom-4 z-30 block rounded-md border border-linha bg-papel p-4 text-left text-[15px] font-normal leading-snug text-texto shadow-xl sm:absolute sm:inset-x-auto sm:bottom-auto sm:left-0 sm:top-full sm:mt-2 sm:w-80 sm:p-3">
          <strong className="block font-serif text-marinho">{termo.termo}</strong>
          <span className="mt-1 block">{termo.explicacao}</span>
          {termo.exemplo && <span className="mt-2 block text-suave">Exemplo: {termo.exemplo}</span>}
        </span>
      )}
    </span>
  )
}

// ------------------------------------------------------------------ estrutura
export function Cabecalho({ aoInicio }: { aoInicio?: () => void }) {
  return (
    <header className="nao-imprimir bg-marinho text-marfim">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4 sm:px-6">
        <button type="button" onClick={aoInicio} className="flex items-center gap-3 text-left">
          <Escudo />
          <span>
            <span className="block font-serif text-xl tracking-wide">{MARCA.nome}</span>
            <span className="hidden text-sm text-marfim/70 sm:block">{MARCA.subtitulo}</span>
          </span>
        </button>
        <span className="hidden text-sm text-marfim/70 md:block">Nada do que você digita é guardado</span>
      </div>
      <div className="h-1 bg-dourado/70" />
    </header>
  )
}

export function Escudo({ className = 'h-9 w-9' }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden="true">
      <path d="M16 4l9 3.4v6.8c0 5.7-3.8 10.5-9 12.4-5.2-1.9-9-6.7-9-12.4V7.4L16 4z" fill="none" stroke="#C9A66B" strokeWidth="2" />
      <path d="M11.5 16l3.2 3.2 5.8-6.6" fill="none" stroke="#F6F4EF" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function Pagina({ children }: { children: ReactNode }) {
  return <main className="mx-auto w-full max-w-5xl px-4 pb-16 pt-6 sm:px-6 sm:pt-10">{children}</main>
}

export function Passos({ atual, nomes }: { atual: number; nomes: string[] }) {
  return (
    <nav aria-label="Etapas" className="nao-imprimir mb-8">
      <ol className="flex gap-1.5">
        {nomes.map((n, i) => (
          <li key={n} className="flex-1">
            <div className={`h-1.5 rounded-full ${i <= atual ? 'bg-acao' : 'bg-linha'}`} />
            <span className={`mt-2 hidden text-xs sm:block ${i === atual ? 'font-semibold text-marinho' : 'text-suave'}`}>{n}</span>
          </li>
        ))}
      </ol>
      <p className="mt-2 text-sm text-suave sm:hidden">Etapa {atual + 1} de {nomes.length}: {nomes[atual]}</p>
    </nav>
  )
}

export function Cartao({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <section className={`rounded-lg border border-linha bg-papel p-5 shadow-sm sm:p-7 ${className}`}>{children}</section>
}

export function Ajuda({ titulo = 'Por que isso importa?', children }: { titulo?: string; children: ReactNode }) {
  return (
    <details className="group mt-2 text-[15px]">
      <summary className="cursor-pointer list-none text-acao hover:underline">
        <span className="mr-1 inline-block transition group-open:rotate-90">›</span>{titulo}
      </summary>
      <div className="mt-2 border-l-2 border-dourado/60 pl-3 text-suave">{children}</div>
    </details>
  )
}

export function ParaOTecnico({ children }: { children: ReactNode }) {
  return (
    <details className="mt-4 rounded-md bg-marfim px-4 py-2 text-sm text-suave">
      <summary className="cursor-pointer select-none font-semibold text-marinho-claro">Para o técnico</summary>
      <div className="mt-2 pb-2">{children}</div>
    </details>
  )
}

type BotaoProps = { children: ReactNode; onClick?: () => void; tipo?: 'primario' | 'secundario'; desativado?: boolean; submit?: boolean }
export function Botao({ children, onClick, tipo = 'primario', desativado, submit }: BotaoProps) {
  const base = 'inline-flex min-h-12 items-center justify-center rounded-md px-6 font-semibold transition disabled:cursor-not-allowed disabled:opacity-50'
  const estilo = tipo === 'primario'
    ? 'bg-acao text-white hover:bg-acao-escuro'
    : 'border border-marinho/30 bg-papel text-marinho hover:border-marinho'
  return <button type={submit ? 'submit' : 'button'} onClick={onClick} disabled={desativado} className={`${base} ${estilo}`}>{children}</button>
}

export function Navegacao({ voltar, avancar, rotuloAvancar = 'Continuar', desativado, carregando }:
  { voltar?: () => void; avancar: () => void; rotuloAvancar?: string; desativado?: boolean; carregando?: boolean }) {
  return (
    <div className="nao-imprimir mt-8 flex flex-col-reverse gap-3 sm:flex-row sm:justify-between">
      {voltar ? <Botao tipo="secundario" onClick={voltar}>Voltar</Botao> : <span />}
      <Botao onClick={avancar} desativado={desativado || carregando}>{carregando ? 'Calculando...' : rotuloAvancar}</Botao>
    </div>
  )
}

export function Erro({ mensagem }: { mensagem: string | null }) {
  if (!mensagem) return null
  return <p role="alert" className="mt-4 rounded-md border border-risco-vermelho/40 bg-risco-vermelho/10 px-4 py-3 text-risco-vermelho">{mensagem}</p>
}

/** Lista de opções como cartões de rádio, com toque grande no celular. */
export function Opcoes<T extends string>({ nome, opcoes, valor, aoEscolher, colunas = 1 }:
  { nome: string; opcoes: { id: T; rotulo: ReactNode; detalhe?: ReactNode }[]; valor: T | null; aoEscolher: (v: T) => void; colunas?: 1 | 2 }) {
  return (
    <div role="radiogroup" className={`mt-4 grid gap-2.5 ${colunas === 2 ? 'sm:grid-cols-2' : ''}`}>
      {opcoes.map((o) => {
        const sel = valor === o.id
        return (
          <label key={o.id}
            className={`flex cursor-pointer items-start gap-3 rounded-md border px-4 py-3 transition ${sel ? 'border-acao bg-acao/5 ring-1 ring-acao' : 'border-linha bg-papel hover:border-marinho/40'}`}>
            <input type="radio" name={nome} className="mt-1.5 h-4 w-4 accent-[#0e5e57]" checked={sel} onChange={() => aoEscolher(o.id)} />
            <span>
              <span className="block">{o.rotulo}</span>
              {o.detalhe && <span className="mt-0.5 block text-sm text-suave">{o.detalhe}</span>}
            </span>
          </label>
        )
      })}
    </div>
  )
}

export function Pergunta({ titulo, ajuda, children }: { titulo: string; ajuda?: string; children: ReactNode }) {
  return (
    <div className="mb-8 last:mb-0">
      <h3 className="font-sans text-lg font-semibold leading-snug text-texto"><Texto>{titulo}</Texto></h3>
      {ajuda && <Ajuda><Texto>{ajuda}</Texto></Ajuda>}
      {children}
    </div>
  )
}
