import { useState, type ReactNode } from 'react'
import { api, ErroApi, type Acao, type Catalogo, type ResultadoCenario, type Simulacao } from '../api'
import { Botao, Cartao, Erro, ParaOTecnico, Texto } from '../componentes/base'
import { pct, reais, reaisCurto } from '../formato'
import { MARCA } from '../marca'
import type { Estado } from '../estado'

type Props = { cat: Catalogo; e: Estado; mudar: (p: Partial<Estado>) => void; refazer: () => void; recomecar: () => void }

const COR_FUNDO = { verde: 'bg-risco-verde/20', amarelo: 'bg-risco-amarelo/30', vermelho: 'bg-risco-vermelho/20' }
const COR_FAIXA = { verde: 'bg-risco-verde', amarelo: 'bg-risco-amarelo', vermelho: 'bg-risco-vermelho' }
const nomeCurto = (n: string) => n.replace(/\s*\(.*\)\s*$/, '')

export function Resultado({ cat, e, mudar, refazer, recomecar }: Props) {
  const s = e.simulacao!
  const r = s.resultado
  const h = r.horizonte_anos
  const conceito = (id: string) => cat.glossario.conceitos.find((c) => c.id === id)
  const descricao = (id: string) => cat.cenarios.find((c) => c.id === id)?.descricao ?? ''
  const ordem = [...r.cenarios].sort((a, b) =>
    (b.nivel_impacto + b.nivel_probabilidade) - (a.nivel_impacto + a.nivel_probabilidade) || b.p90_quando_ocorre - a.p90_quando_ocorre)

  return (
    <>
      <section className="faixa-inteira -mt-6 bg-marinho px-4 pb-10 pt-10 text-marfim sm:-mt-10 sm:px-6">
        <div className="mx-auto max-w-5xl">
          <p className="text-sm uppercase tracking-[0.18em] text-dourado">Resultado · {s.porte.nome}</p>
          <h1 className="mt-2 font-serif text-3xl text-marfim sm:text-4xl">O risco digital da sua empresa, em reais</h1>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            <Numero titulo={`Chance de algum prejuízo nos próximos ${h} anos`} valor={pct(r.chance_algum_prejuizo_horizonte)}
              nota={`${pct(r.chance_algum_prejuizo)} a cada ano`} />
            <Numero titulo="Perda média esperada por ano" valor={reais(r.perda_esperada_total)}
              nota="Soma de todos os riscos, considerando a chance de cada um" />
            <Numero titulo={`Prejuízo em um período ruim de ${h} anos`} valor={reaisCurto(s.plano.perda_periodo_ruim_atual)}
              nota="Só é ultrapassado em 1 de cada 10 cenários simulados" />
          </div>
          <p className="mt-6 text-[15px] text-marfim/70">
            Seus limites: perdas até {reais(r.apetite_rs)} por ano são aceitáveis; a partir de {reais(r.tolerancia_rs)}, a
            continuidade da empresa fica ameaçada.
          </p>
        </div>
      </section>

      <div className="mx-auto mt-8 max-w-5xl space-y-6">
        <Cartao>
          <h2 className="text-2xl">Mapa de calor</h2>
          <p className="mt-1 text-suave">{conceito('mapa_calor')?.explicacao}</p>
          <Mapa cat={cat} s={s} />
          {r.cenarios.some((c) => c.destaque) && <p className="mt-3 text-sm text-suave">★ Ligado ao que você apontou como mais importante para a empresa.</p>}
        </Cartao>

        <Cartao>
          <h2 className="text-2xl">Os riscos, um a um</h2>
          <div className="mt-5 space-y-4">
            {ordem.map((c) => <CenarioCartao key={c.id} c={c} cat={cat} s={s} descricao={descricao(c.id)} />)}
          </div>
        </Cartao>

        <Plano s={s} />

        {r.nao_sei.length > 0 && (
          <Cartao>
            <h2 className="text-2xl">Pontos que vale descobrir</h2>
            <p className="mt-1 text-suave">
              Nestas perguntas você respondeu "Não sei". A ferramenta considerou a situação mais cautelosa; descobrir a
              resposta pode melhorar o resultado.
            </p>
            <ul className="mt-4 list-disc space-y-2 pl-6">
              {r.nao_sei.map((id) => <li key={id}><Texto>{e.questionario?.perguntas.find((p) => p.id === id)?.texto ?? id}</Texto></li>)}
            </ul>
          </Cartao>
        )}

        <Contribuicao e={e} mudar={mudar} s={s} />

        <div className="nao-imprimir flex flex-col gap-3 sm:flex-row">
          <Botao onClick={() => window.print()}>Salvar em PDF ou imprimir</Botao>
          <Botao tipo="secundario" onClick={refazer}>Revisar respostas</Botao>
          <Botao tipo="secundario" onClick={recomecar}>Apagar tudo e recomeçar</Botao>
        </div>
        <p className="text-sm text-suave">{cat.aviso_legal}</p>
        <p className="text-xs text-suave">{MARCA.nome} · catálogo {s.versao_catalogo} · {r.iteracoes.toLocaleString('pt-BR')} anos simulados</p>
      </div>
    </>
  )
}

function Numero({ titulo, valor, nota }: { titulo: string; valor: string; nota: string }) {
  return (
    <div className="rounded-lg border border-marfim/15 bg-marinho-claro/60 p-5">
      <p className="text-sm text-marfim/70">{titulo}</p>
      <p className="mt-1 font-serif text-3xl text-marfim sm:text-4xl">{valor}</p>
      <p className="mt-1 text-sm text-marfim/60">{nota}</p>
    </div>
  )
}

// ------------------------------------------------------------------ mapa 3 × 3
function Mapa({ cat, s }: { cat: Catalogo; s: Simulacao }) {
  const m = cat.matriz
  const cor = (i: number, j: number) => m.cores.find((c) => c.soma.includes(i + j))!.cor
  const porId = Object.fromEntries(s.resultado.cenarios.map((c) => [c.id, c]))
  return (
    <div className="mt-6">
      <div className="grid grid-cols-[auto_1fr] gap-2">
        <div className="flex items-center"><span className="-rotate-180 text-xs uppercase tracking-wider text-suave [writing-mode:vertical-rl]">Impacto</span></div>
        <div className="grid grid-cols-3 gap-1.5 sm:gap-2">
          {[3, 2, 1].flatMap((i) => [1, 2, 3].map((j) => {
            const ids = s.matriz.celulas[`${i},${j}`] ?? []
            return (
              <div key={`${i}${j}`} className={`min-h-24 rounded-md p-1.5 sm:min-h-28 sm:p-2.5 ${COR_FUNDO[cor(i, j)]}`}>
                {j === 1 && <p className="mb-1 text-[11px] leading-tight text-suave sm:text-xs">{m.impacto.find((x) => x.nivel === i)?.rotulo}</p>}
                <div className="flex flex-col gap-1">
                  {ids.map((id) => {
                    const c = porId[id]
                    return (
                      <a key={id} href={`#cen-${id}`}
                        className="rounded border border-black/10 bg-papel px-1.5 py-1 text-[12px] leading-tight shadow-sm hover:border-marinho sm:text-sm">
                        {c.destaque && <span className="text-dourado">★ </span>}{nomeCurto(c.nome)}
                        {c.ruptura && <span className="mt-0.5 block text-[11px] font-semibold text-risco-vermelho">risco de ruptura</span>}
                      </a>
                    )
                  })}
                </div>
              </div>
            )
          }))}
        </div>
        <span />
        <div className="grid grid-cols-3 gap-2 text-center text-[11px] leading-tight text-suave sm:text-xs">
          {m.probabilidade.map((p) => <span key={p.nivel}>{p.rotulo}</span>)}
        </div>
        <span />
        <p className="text-center text-xs uppercase tracking-wider text-suave">Chance de acontecer</p>
      </div>
      <ul className="mt-5 flex flex-wrap gap-x-5 gap-y-2 text-sm">
        {m.cores.map((c) => (
          <li key={c.cor} className="flex items-center gap-2"><span className={`h-3 w-3 rounded-sm ${COR_FAIXA[c.cor]}`} />{c.significado}</li>
        ))}
      </ul>
    </div>
  )
}

// ------------------------------------------------------------------ cenários
function CenarioCartao({ c, cat, s, descricao }: { c: ResultadoCenario; cat: Catalogo; s: Simulacao; descricao: string }) {
  const rup = s.plano.ruptura.find((x) => x.cenario === c.id)
  const nomes = Object.fromEntries(s.plano.acoes.map((a) => [a.controle, a.titulo]))
  const impRot = cat.matriz.impacto.find((x) => x.nivel === c.nivel_impacto)?.rotulo
  const probRot = cat.matriz.probabilidade.find((x) => x.nivel === c.nivel_probabilidade)?.rotulo
  return (
    <article id={`cen-${c.id}`} className="scroll-mt-6 overflow-hidden rounded-md border border-linha">
      <div className={`h-1.5 ${COR_FAIXA[c.cor]}`} />
      <div className="p-4 sm:p-5">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h3 className="text-xl">{c.destaque && <span className="text-dourado">★ </span>}{c.nome}</h3>
          <span className="text-sm text-suave">{impRot} · {probRot}</span>
        </div>
        <p className="mt-1 text-[15px] text-suave">{descricao}</p>
        <dl className="mt-4 grid gap-3 text-[15px] sm:grid-cols-3">
          <div><dt className="text-suave">Chance em {s.resultado.horizonte_anos} anos</dt><dd className="text-lg font-semibold">{pct(c.chance_horizonte)}</dd></div>
          <div><dt className="text-suave">Prejuízo em um ano em que acontece</dt><dd className="text-lg font-semibold">até {reais(c.p90_quando_ocorre)}</dd></div>
          <div><dt className="text-suave">Perda média por ano</dt><dd className="text-lg font-semibold">{reais(c.perda_esperada)}</dd></div>
        </dl>
        {rup && (
          <div className="mt-4 rounded-md border-l-4 border-risco-vermelho bg-risco-vermelho/5 p-4 text-[15px]">
            <p><Texto>{rup.texto}</Texto></p>
            <p className="mt-2">
              Com as medidas de preparação, o prejuízo em um ano em que isso acontece cai de <strong>{reais(rup.impacto_atual)}</strong> para{' '}
              <strong>{reais(rup.impacto_com_preparacao)}</strong>.{' '}
              {rup.sai_da_ruptura
                ? 'Isso fica abaixo do limite que a empresa aguenta.'
                : `Ainda fica acima do limite que a empresa aguenta (${reais(rup.tolerancia)}), por isso vale considerar também transferir parte do risco.`}
            </p>
            {rup.preparacao.length > 0 && (
              <p className="mt-2 text-suave">Medidas de preparação: {rup.preparacao.map((id) => nomes[id] ?? id).join('; ')}.</p>
            )}
            <p className="mt-2"><Texto>{rup.transferencia}</Texto></p>
          </div>
        )}
        <ParaOTecnico>
          <ul className="space-y-0.5">
            <li>Frequência de eventos de perda (LEF): {c.lef.toFixed(4)}/ano · vulnerabilidade {c.vulnerabilidade.toFixed(3)}</li>
            <li>Maturidade de prevenção {pct(c.maturidade)} · de resposta {pct(c.maturidade_resposta)}</li>
            <li>Fatores de magnitude: primária {c.fator_primaria.toFixed(3)} · secundária {c.fator_secundaria.toFixed(3)}</li>
            <li>Chance anual {pct(c.chance_ano)} · P90 condicional {reais(c.p90_quando_ocorre)} · célula ({c.nivel_impacto}, {c.nivel_probabilidade})</li>
          </ul>
        </ParaOTecnico>
      </div>
    </article>
  )
}

// ------------------------------------------------------------------ plano de ação
function Plano({ s }: { s: Simulacao }) {
  const p = s.plano
  const nomeCen = Object.fromEntries(s.resultado.cenarios.map((c) => [c.id, nomeCurto(c.nome)]))
  const dentro = p.acoes.filter((a) => !a.acima_do_limite)
  const preparo = p.acoes.filter((a) => a.acima_do_limite && a.protege_ruptura.length > 0)
  const fora = p.acoes.filter((a) => a.acima_do_limite && a.protege_ruptura.length === 0)
  return (
    <Cartao className="quebra-antes">
      <h2 className="text-2xl">Plano de ação</h2>
      {p.acoes.length === 0 ? (
        <p className="mt-2 text-suave">Pelas respostas, a empresa já faz o que este questionário cobre. Mantenha as práticas e revise uma vez por ano.</p>
      ) : (
        <>
          <p className="mt-1 text-suave">
            As medidas estão em ordem: primeiro as que mais compensam pelo custo. Vale a pena investir até cerca de{' '}
            <strong className="text-texto">{reais(p.limite_investimento)} por ano</strong> em proteção, somando as medidas.
            Esse limite vem do modelo de Gordon e Loeb: acima dele, a proteção tende a custar mais do que evita.
          </p>
          <h3 className="mt-8 font-sans text-sm font-semibold uppercase tracking-[0.14em] text-acao">Comece por aqui</h3>
          <div className="mt-3 space-y-4">
            {dentro.length ? dentro.map((a) => <AcaoCartao key={a.controle} a={a} nomeCen={nomeCen} h={p.horizonte_anos} />)
              : <p className="text-suave">Nenhuma medida cabe sozinha no limite de investimento; comece pelas de proteção contra ruptura abaixo.</p>}
          </div>
          {preparo.length > 0 && (
            <>
              <h3 className="mt-10 font-sans text-sm font-semibold uppercase tracking-[0.14em] text-risco-vermelho">Prepare-se para o pior caso</h3>
              <p className="mt-1 text-[15px] text-suave">
                Pela média, estas medidas parecem caras. Mas elas diminuem o prejuízo dos riscos de ruptura, aqueles raros que,
                se acontecerem, podem ameaçar a empresa. Funcionam como um seguro: vale avaliar mesmo passando do limite.
              </p>
              <div className="mt-3 space-y-3">
                {preparo.map((a) => <AcaoCartao key={a.controle} a={a} nomeCen={nomeCen} h={p.horizonte_anos} recolhida />)}
              </div>
            </>
          )}
          {fora.length > 0 && (
            <>
              <h3 className="mt-10 font-sans text-sm font-semibold uppercase tracking-[0.14em] text-suave">Avalie depois</h3>
              <p className="mt-1 text-[15px] text-suave">Somadas às anteriores, passam do limite de investimento. Retome quando as primeiras estiverem funcionando.</p>
              <div className="mt-3 space-y-3">
                {fora.map((a) => <AcaoCartao key={a.controle} a={a} nomeCen={nomeCen} h={p.horizonte_anos} recolhida />)}
              </div>
            </>
          )}
        </>
      )}
      <ParaOTecnico>
        Perda esperada atual {reais(p.perda_esperada_atual)}/ano; limite de Gordon-Loeb = perda esperada ÷ e. Ordem: medidas
        sem custo, depois retorno sobre o investimento (ROSI) decrescente. Redução no período ruim = queda do P90 da perda
        somada em {p.horizonte_anos} anos.
      </ParaOTecnico>
    </Cartao>
  )
}

function AcaoCartao({ a, nomeCen, h, recolhida }: { a: Acao; nomeCen: Record<string, string>; h: number; recolhida?: boolean }) {
  const selos = (
    <div className="flex flex-wrap gap-2">
      {a.protege_ruptura.length > 0 && <Selo cor="vermelho">Protege contra ruptura: {a.protege_ruptura.map((c) => nomeCen[c]).join(', ')}</Selo>}
      {a.selo && <Selo cor="dourado">Privacidade</Selo>}
      {a.custo_anual === 0 && <Selo cor="verde">Sem custo</Selo>}
    </div>
  )
  const corpo = (
    <>
      {a.selo && <p className="mt-3 text-[15px] text-suave">{a.selo}</p>}
      <ul className="mt-3 space-y-3">
        {a.recomendacoes.map((t, i) => <li key={i} className="text-[15px]"><Texto>{t}</Texto></li>)}
      </ul>
      <p className="mt-4 text-[15px]">
        Reduz a perda média em <strong>{reais(a.reducao_perda_anual)} por ano</strong>
        {a.reducao_periodo_ruim > 0 && <> e o prejuízo em um período ruim de {h} anos em <strong>{reais(a.reducao_periodo_ruim)}</strong></>}.
        {' '}Custo estimado: <strong>{a.custo_anual === 0 ? 'sem custo' : `${reais(a.custo_anual)} por ano`}</strong>.
      </p>
      <ParaOTecnico>
        Controle ISO/IEC 27002 {a.controle} ({a.controle_nome}) · perguntas {a.perguntas.join(', ')} · ROSI {a.rosi === null ? 'n/d (sem custo)' : pct(a.rosi)}
        {Object.keys(a.impacto_ruptura).length > 0 && <> · impacto com a medida: {Object.entries(a.impacto_ruptura).map(([c, v]) => `${c} ${reais(v)}`).join(', ')}</>}
      </ParaOTecnico>
    </>
  )
  if (recolhida) {
    return (
      <details className="group rounded-md border border-linha bg-papel">
        <summary className="flex cursor-pointer list-none flex-col gap-2 p-4 sm:flex-row sm:items-center sm:justify-between">
          <span className="font-semibold">{a.titulo}</span>
          {selos}
        </summary>
        <div className="border-t border-linha px-4 pb-4">{corpo}</div>
      </details>
    )
  }
  return (
    <article className="rounded-md border border-linha bg-papel p-4 sm:p-5">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <h4 className="font-serif text-lg text-marinho"><span className="mr-2 text-dourado">{a.prioridade}.</span>{a.titulo}</h4>
        {selos}
      </div>
      {corpo}
    </article>
  )
}

function Selo({ cor, children }: { cor: 'vermelho' | 'dourado' | 'verde'; children: ReactNode }) {
  const c = { vermelho: 'border-risco-vermelho/40 text-risco-vermelho', dourado: 'border-dourado/60 text-[#7d6136]', verde: 'border-risco-verde/50 text-risco-verde' }[cor]
  return <span className={`rounded-full border bg-papel px-2.5 py-0.5 text-xs font-semibold ${c}`}>{children}</span>
}

// ------------------------------------------------------------------ contribuição anonimizada (ADR-005)
function Contribuicao({ e, mudar, s }: { e: Estado; mudar: (p: Partial<Estado>) => void; s: Simulacao }) {
  const [aceito, setAceito] = useState(false)
  const [erro, setErro] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)
  if (e.contribuiu) {
    return <Cartao className="nao-imprimir"><p>Obrigado! Suas respostas anônimas foram registradas para a pesquisa.</p></Cartao>
  }
  async function enviar() {
    setErro(null)
    setEnviando(true)
    try {
      await api.contribuir(e.setor!, s.porte.nivel, e.respostas, s.comprovante_contribuicao, s.resumo_pesquisa)
      mudar({ contribuiu: true })
    } catch (x) {
      setErro(x instanceof ErroApi && /não está ativa/.test(x.message) ? 'A coleta para pesquisa não está ativa neste momento.'
        : x instanceof ErroApi && x.status === 503 ? 'Não foi possível registrar agora. Tente de novo em alguns minutos.'
          : x instanceof ErroApi ? x.message : 'Não foi possível enviar. Tente de novo.')
    } finally {
      setEnviando(false)
    }
  }
  return (
    <Cartao className="nao-imprimir">
      <h2 className="text-xl">Quer ajudar a pesquisa?</h2>
      <p className="mt-2 text-[15px] text-suave">
        Esta ferramenta faz parte de um trabalho de conclusão de curso na UFMG. Se você autorizar, enviamos só o setor, o
        porte, as respostas do questionário e o resultado sem valores em reais: a posição de cada risco no mapa e as
        medidas recomendadas. Nunca a receita, valores em reais, número de pessoas ou qualquer dado que identifique a
        empresa. Os dados são analisados só em conjunto e apagados depois da aprovação do trabalho.
      </p>
      <label className="mt-4 flex items-start gap-3">
        <input type="checkbox" className="mt-1 h-4 w-4 accent-[#0e5e57]" checked={aceito} onChange={(ev) => setAceito(ev.target.checked)} />
        <span>Autorizo o uso anônimo das minhas respostas para pesquisa acadêmica.</span>
      </label>
      <div className="mt-4"><Botao onClick={enviar} desativado={!aceito || enviando}>{enviando ? 'Enviando...' : 'Enviar respostas anônimas'}</Botao></div>
      <Erro mensagem={erro} />
    </Cartao>
  )
}
