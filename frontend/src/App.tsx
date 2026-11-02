import { useEffect, useState } from 'react'
import { api, ErroApi, type Catalogo } from './api'
import { Cabecalho, Erro, Pagina, Passos, ProvedorGlossario } from './componentes/base'
import { apagar, carregar, INICIAL, montarPerfil, salvar, type Estado, type Etapa } from './estado'
import { Ativos, Empresa, Financeiro, Inicio } from './telas/entrada'
import { Questionario } from './telas/questionario'
import { Resultado } from './telas/resultado'

const ETAPAS: Etapa[] = ['empresa', 'financeiro', 'ativos', 'questionario', 'resultado']
const NOMES = ['Empresa', 'Dinheiro e limites', 'O que proteger', 'Como é hoje', 'Resultado']

export default function App() {
  const [cat, setCat] = useState<Catalogo | null>(null)
  const [erroCat, setErroCat] = useState<string | null>(null)
  const [e, setE] = useState<Estado>(carregar)
  const [carregando, setCarregando] = useState(false)
  const [erroSim, setErroSim] = useState<string | null>(null)
  const [temSessao] = useState(() => e.etapa !== 'inicio' || Boolean(e.setor))

  useEffect(() => {
    api.catalogo().then(setCat).catch((x) => setErroCat(x instanceof ErroApi ? x.message : 'Não foi possível carregar.'))
  }, [])
  useEffect(() => { salvar(e) }, [e])

  const mudar = (p: Partial<Estado>) => setE((atual) => ({ ...atual, ...p }))
  const ir = (etapa: Etapa) => { mudar({ etapa }); window.scrollTo({ top: 0 }) }

  async function simular() {
    const perfil = montarPerfil(e)
    if (!perfil) return setErroSim('Falta alguma resposta nas etapas anteriores. Volte e confira.')
    setErroSim(null)
    setCarregando(true)
    try {
      const s = await api.simular(perfil, e.respostas)
      mudar({ simulacao: s, etapa: 'resultado', contribuiu: false })
      window.scrollTo({ top: 0 })
    } catch (x) {
      setErroSim(x instanceof ErroApi ? x.message : 'Algo deu errado no cálculo. Tente de novo.')
    } finally {
      setCarregando(false)
    }
  }

  function recomecar() {
    apagar()
    setE(INICIAL)
    window.scrollTo({ top: 0 })
  }

  if (!cat) {
    return (
      <>
        <Cabecalho />
        <Pagina>{erroCat ? <Erro mensagem={erroCat} /> : <p className="text-suave">Carregando...</p>}</Pagina>
      </>
    )
  }

  const indice = ETAPAS.indexOf(e.etapa)
  const etapa = e.etapa === 'resultado' && !e.simulacao ? 'questionario' : e.etapa
  const props = { cat, e, mudar }
  return (
    <ProvedorGlossario termos={cat.glossario.termos}>
      <Cabecalho aoInicio={() => ir('inicio')} />
      <Pagina>
        {indice >= 0 && etapa !== 'resultado' && <Passos atual={indice} nomes={NOMES} />}
        {etapa === 'inicio' && <Inicio cat={cat} comecar={() => { recomecar(); ir('empresa') }} temSessao={temSessao}
          continuar={() => ir(e.simulacao ? 'resultado' : e.questionario ? 'questionario' : 'empresa')} />}
        {etapa === 'empresa' && <Empresa {...props} voltar={() => ir('inicio')} avancar={() => ir('financeiro')} />}
        {etapa === 'financeiro' && <Financeiro {...props} voltar={() => ir('empresa')} avancar={() => ir('ativos')} />}
        {etapa === 'ativos' && <Ativos {...props} voltar={() => ir('financeiro')} avancar={() => ir('questionario')} />}
        {etapa === 'questionario' && <Questionario {...props} voltar={() => ir('ativos')} concluir={simular} carregando={carregando} erro={erroSim} />}
        {etapa === 'resultado' && <Resultado {...props} refazer={() => ir('empresa')} recomecar={recomecar} />}
      </Pagina>
      <footer className="nao-imprimir border-t border-linha bg-papel">
        <div className="mx-auto max-w-5xl px-4 py-6 text-sm text-suave sm:px-6">
          Ferramenta acadêmica desenvolvida em trabalho de conclusão de curso na UFMG, com base na ABNT NBR ISO/IEC 27005 e
          no método FAIR. Valores financeiros e dados da empresa nunca são guardados; as respostas do questionário e o resultado, sem valores em reais, só são guardados, sem identificação, se você autorizar no final.
        </div>
      </footer>
    </ProvedorGlossario>
  )
}
