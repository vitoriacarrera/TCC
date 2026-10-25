import { useState } from 'react'
import { api, ErroApi, type Catalogo, type PerguntaContexto } from '../api'
import { Ajuda, Botao, Cartao, Erro, Escudo, Navegacao, Opcoes, Pergunta, Texto } from '../componentes/base'
import { digitarMoeda, reais } from '../formato'
import { MARCA } from '../marca'
import { receita, usuarios, type Estado } from '../estado'

type Props = { cat: Catalogo; e: Estado; mudar: (p: Partial<Estado>) => void }

const pergunta = (cat: Catalogo, id: string): PerguntaContexto =>
  [...cat.contexto.financeiro, ...cat.contexto.ativos, ...cat.contexto.calibracao_risco].find((q) => q.id === id)!

// ------------------------------------------------------------------ início
export function Inicio({ cat, comecar, temSessao, continuar }:
  { cat: Catalogo; comecar: () => void; temSessao: boolean; continuar: () => void }) {
  const min = Object.values(cat.instrucoes.tempo_estimado_min)
  return (
    <>
      <section className="faixa-inteira -mt-6 bg-marinho px-4 pb-14 pt-12 text-marfim sm:-mt-10 sm:px-6 sm:pt-16">
        <div className="mx-auto max-w-3xl">
          <p className="text-sm uppercase tracking-[0.18em] text-dourado">{MARCA.publico}</p>
          <h1 className="mt-3 font-serif text-4xl leading-tight text-marfim sm:text-5xl">
            Quanto um problema digital pode custar à sua empresa, e por onde começar a se proteger
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-marfim/80">
            Em poucos minutos, o {MARCA.nome} estima em reais o prejuízo que ataques e falhas podem causar, mostra quais
            riscos olhar primeiro e monta um plano de ação com o custo de cada medida.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Botao onClick={comecar}>Começar a análise</Botao>
            {temSessao && <Botao tipo="secundario" onClick={continuar}>Continuar de onde parei</Botao>}
          </div>
          <p className="mt-4 text-sm text-marfim/60">Leva de {Math.min(...min)} a {Math.max(...min)} minutos, conforme o tamanho da empresa.</p>
        </div>
      </section>
      <div className="mx-auto mt-10 grid max-w-5xl gap-4 sm:grid-cols-3">
        {[
          ['1. Conte sobre a empresa', 'Setor, receita aproximada e quanto a empresa aguenta perder num ano ruim.'],
          ['2. Responda como é hoje', 'Perguntas simples sobre senhas, cópias de segurança, fornecedores e o que fazer num problema.'],
          ['3. Receba o plano', 'Mapa dos riscos, prejuízo estimado em reais e as medidas que mais compensam para o seu caso.'],
        ].map(([t, d]) => (
          <Cartao key={t}><h2 className="text-xl">{t}</h2><p className="mt-2 text-suave">{d}</p></Cartao>
        ))}
      </div>
      <div className="mx-auto mt-6 flex max-w-5xl items-start gap-3 rounded-lg border border-linha bg-papel p-5 text-[15px] text-suave">
        <Escudo className="mt-0.5 h-6 w-6 shrink-0 [&_path:first-child]:stroke-marinho [&_path:last-child]:stroke-acao" />
        <p>
          <strong className="text-texto">Sua privacidade:</strong> não pedimos nome, CNPJ nem e-mail. A receita e os outros
          valores servem só para o cálculo e somem quando você fecha esta aba. No final, você pode autorizar que as respostas
          do questionário sejam guardadas sem identificação, junto com o setor e o porte, para a pesquisa do trabalho. Sem
          a sua autorização, nada é guardado.
        </p>
      </div>
      <p className="mx-auto mt-6 max-w-5xl text-sm text-suave">{cat.aviso_legal}</p>
    </>
  )
}

// ------------------------------------------------------------------ 1. empresa
export function Empresa({ cat, e, mudar, voltar, avancar }: Props & { voltar: () => void; avancar: () => void }) {
  const [erro, setErro] = useState<string | null>(null)
  const [carregando, setCarregando] = useState(false)
  const qRob = pergunta(cat, 'receita_operacional_bruta')
  const qUsu = pergunta(cat, 'usuarios_ti')
  const r = receita(e)
  const u = usuarios(e)

  async function seguir() {
    setErro(null)
    if (!e.setor || !r || !u) return setErro('Preencha o setor, a receita e o número de pessoas para continuar.')
    setCarregando(true)
    try {
      const q = await api.questionario(e.setor, r, u)
      const mudouPerfil = e.questionario && (e.questionario.porte.nivel !== q.porte.nivel
        || e.questionario.perguntas.map((p) => p.id).join() !== q.perguntas.map((p) => p.id).join())
      mudar({ questionario: q, ...(mudouPerfil ? { respostas: {}, grupo: 0, simulacao: null } : {}) })
      avancar()
    } catch (x) {
      setErro(x instanceof ErroApi ? x.message : 'Algo deu errado. Tente de novo.')
    } finally {
      setCarregando(false)
    }
  }

  return (
    <Cartao>
      <h2 className="text-2xl sm:text-3xl">Sobre a empresa</h2>
      <p className="mt-2 text-suave">Essas respostas ajustam a análise ao tamanho e ao tipo do negócio.</p>
      <div className="mt-8">
        <Pergunta titulo="Em qual setor a empresa atua?">
          <Opcoes nome="setor" colunas={2} valor={e.setor} aoEscolher={(v) => mudar({ setor: v })}
            opcoes={cat.setores.map((s) => ({ id: s.id, rotulo: <strong className="font-semibold">{s.nome}</strong>, detalhe: s.exemplos }))} />
        </Pergunta>
        <Pergunta titulo={qRob.texto} ajuda={qRob.ajuda}>
          {qRob.como_calcular && <Ajuda titulo="Como calcular"><Texto>{qRob.como_calcular}</Texto></Ajuda>}
          {qRob.onde_encontrar && <Ajuda titulo="Onde encontrar esse valor"><Texto>{qRob.onde_encontrar}</Texto></Ajuda>}
          <CampoMoeda id="receita" valor={e.receitaTexto} aoMudar={(v) => mudar({ receitaTexto: v })} />
        </Pergunta>
        <Pergunta titulo={qUsu.texto} ajuda={qUsu.ajuda}>
          <input id="usuarios" inputMode="numeric" value={e.usuariosTexto} placeholder="Ex.: 8"
            onChange={(ev) => mudar({ usuariosTexto: ev.target.value.replace(/\D/g, '').slice(0, 6) })}
            className="mt-4 block w-40 rounded-md border border-linha bg-papel px-4 py-3 text-lg focus:border-acao" />
        </Pergunta>
      </div>
      <Erro mensagem={erro} />
      <Navegacao voltar={voltar} avancar={seguir} carregando={carregando} desativado={!e.setor || !r || !u} />
    </Cartao>
  )
}

function CampoMoeda({ id, valor, aoMudar }: { id: string; valor: string; aoMudar: (v: string) => void }) {
  return (
    <div className="mt-4 flex max-w-xs items-center rounded-md border border-linha bg-papel focus-within:border-acao">
      <span className="pl-4 text-suave">R$</span>
      <input id={id} inputMode="numeric" autoComplete="off" value={valor} placeholder="0"
        onChange={(ev) => aoMudar(digitarMoeda(ev.target.value))}
        className="w-full bg-transparent px-2 py-3 text-lg outline-none" />
    </div>
  )
}

// ------------------------------------------------------------------ 2. financeiro e apetite
export function Financeiro({ cat, e, mudar, voltar, avancar }: Props & { voltar: () => void; avancar: () => void }) {
  const qHora = pergunta(cat, 'custo_hora_parada')
  const qApe = pergunta(cat, 'apetite_pct')
  const qTol = pergunta(cat, 'tolerancia_pct')
  const r = receita(e) ?? 0
  const estimado = r / 2080
  const apetite = qApe.opcoes!.find((o) => o.id === e.apetite)
  const tolerancias = qTol.opcoes!.filter((o) => o.valor_por_setor || !apetite || (o.valor ?? 0) > (apetite.valor ?? 0))
  const tolValida = tolerancias.some((o) => o.id === e.tolerancia)
  const horaOk = e.custoHoraNaoSei || Boolean(e.custoHoraTexto)

  return (
    <Cartao>
      {e.questionario && (
        <p className="mb-6 rounded-md border-l-4 border-dourado bg-marfim px-4 py-3 text-[15px]">{e.questionario.mensagem_porte}</p>
      )}
      <h2 className="text-2xl sm:text-3xl">Dinheiro e limites</h2>
      <p className="mt-2 text-suave">Com isso, a ferramenta traduz cada risco para o tamanho da sua empresa.</p>
      <div className="mt-8">
        <Pergunta titulo={qHora.texto} ajuda={qHora.ajuda}>
          {!e.custoHoraNaoSei && <CampoMoeda id="custo-hora" valor={e.custoHoraTexto} aoMudar={(v) => mudar({ custoHoraTexto: v })} />}
          <label className="mt-3 flex items-center gap-2">
            <input type="checkbox" className="h-4 w-4 accent-[#0e5e57]" checked={e.custoHoraNaoSei}
              onChange={(ev) => mudar({ custoHoraNaoSei: ev.target.checked })} />
            Não sei
          </label>
          {e.custoHoraNaoSei && qHora.mensagem_padrao && (
            <p className="mt-2 text-[15px] text-suave">{qHora.mensagem_padrao.replace('R$ {valor}', reais(estimado))}</p>
          )}
        </Pergunta>
        <Pergunta titulo={qApe.texto} ajuda={qApe.ajuda}>
          <Opcoes nome="apetite" colunas={2} valor={e.apetite} aoEscolher={(v) => mudar({ apetite: v })}
            opcoes={qApe.opcoes!.map((o) => ({ id: o.id, rotulo: o.rotulo, detalhe: o.id !== 'nao_sei' && r ? `cerca de ${reais((o.valor ?? 0) * r)}` : undefined }))} />
        </Pergunta>
        <Pergunta titulo={qTol.texto} ajuda={qTol.ajuda}>
          <Opcoes nome="tolerancia" colunas={2} valor={tolValida ? e.tolerancia : null} aoEscolher={(v) => mudar({ tolerancia: v })}
            opcoes={tolerancias.map((o) => ({ id: o.id, rotulo: o.rotulo, detalhe: !o.valor_por_setor && r ? `cerca de ${reais((o.valor ?? 0) * r)}` : undefined }))} />
          {apetite && apetite.id !== 'nao_sei' && <p className="mt-2 text-sm text-suave">Só aparecem valores acima do que você escolheu na pergunta anterior.</p>}
        </Pergunta>
      </div>
      <Navegacao voltar={voltar} avancar={avancar} desativado={!horaOk || !e.apetite || !tolValida} />
    </Cartao>
  )
}

// ------------------------------------------------------------------ 3. ativos
export function Ativos({ cat, e, mudar, voltar, avancar }: Props & { voltar: () => void; avancar: () => void }) {
  const qs = ['ativo_critico', 'tipo_dado', 'registros_pessoais'].map((id) => pergunta(cat, id))
  const chaves = ['ativo_critico', 'tipo_dado', 'registros_pessoais'] as const
  return (
    <Cartao>
      <h2 className="text-2xl sm:text-3xl">O que a empresa precisa proteger</h2>
      <p className="mt-2 text-suave">Isso destaca no relatório os riscos que mais pesam para o seu negócio.</p>
      <div className="mt-8">
        {qs.map((q, i) => (
          <Pergunta key={q.id} titulo={q.texto} ajuda={q.ajuda}>
            <Opcoes nome={q.id} valor={e[chaves[i]]} aoEscolher={(v) => mudar({ [chaves[i]]: v } as Partial<Estado>)}
              opcoes={q.opcoes!.map((o) => ({ id: o.id, rotulo: <Texto>{o.rotulo}</Texto> }))} />
          </Pergunta>
        ))}
      </div>
      <Navegacao voltar={voltar} avancar={avancar} desativado={chaves.some((k) => !e[k])} />
    </Cartao>
  )
}
