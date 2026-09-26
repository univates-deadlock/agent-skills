# Plano de melhoria das skills de API e Next.js

Data: 2026-09-26

## 1. Resultado da análise

**A skill de backend é compatível com a estrutura atual do TechPro.** Ela orienta
preservar a organização existente, validar entradas, manter HTTP na fronteira,
usar Prisma diretamente quando adequado e aplicar autenticação e autorização no
servidor. Não impõe repositories, classes, Clean Architecture ou outra camada.

A skill de frontend também é compatível com Next.js App Router, React e Tailwind.
Ela cobre limites Server/Client, formulários, integração, responsividade e
acessibilidade. Como o frontend ainda tem a página padrão do Next.js, essa
compatibilidade foi avaliada pela configuração e pelo cliente de autenticação,
não por um fluxo completo de interface implementado.

**Este plano complementa orientações práticas; não propõe substituir a arquitetura
ou reescrever as skills.** O material atual é genérico e algumas decisões exigem
mais interpretação do agente, principalmente em autenticação por biblioteca,
configuração de aplicações separadas e verificação condicionada ao escopo.

O usuário pretende aplicar o plano no repositório oficial das skills e atualizar
as cópias deste projeto depois. Nenhuma skill local foi alterada nesta análise.
Nenhum commit, rename de branch ou publicação foi realizado.

## 2. Material analisado

- `.agents/skills/building-typescript-rest-apis/SKILL.md` e suas quatro referências.
- `.agents/skills/developing-nextjs-app-router-interfaces/SKILL.md` e suas cinco referências.
- Organização atual de `api/src`, Prisma, scripts npm e CI.
- Integração Better Auth, contexto em `res.locals`, validação Zod e erros HTTP.
- `frontend/lib/auth-client.ts`, configuração Next.js e página atual.
- `AGENTS.md`, `CLAUDE.md` e READMEs.

Há duas cópias físicas das skills: `.agents/skills/` e `.claude/skills/`. Elas estão
iguais nesta análise. A atualização futura deve alcançar ambas sem divergência.

Os caminhos abaixo começam no diretório da skill, independentemente de sua
localização no repositório oficial. Não é necessário reproduzir `.agents/` lá.

## 3. Mapeamento de compatibilidade

| Princípio atual da skill | Correspondência no TechPro | Avaliação |
| --- | --- | --- |
| Preservar convenções existentes | `routes`, `controllers`, `schemas`, `services`, `middlewares`, `lib`, `config`, `utils` | Alinhado |
| HTTP na fronteira | Controllers validam requests e respondem; services não recebem Express | Alinhado |
| Validação em tempo de execução | Schemas Zod, envelopes estritos e tipos com `z.infer` | Alinhado |
| Autorização no servidor | Sessão ativa seguida de `requireAdmin` | Alinhado |
| Seleção deliberada de campos | `userSelect` omite credenciais e sessões | Alinhado |
| Transações e concorrência | Revogação atômica, proteção de admin e revalidação de sessão | Alinhado no princípio; pode ganhar referência mais operacional |
| Erros previsíveis sem dados sensíveis | AppError, mapeamento Prisma e Zod | Alinhado; diagnóstico seguro continua importante |
| Reutilizar integração de identidade | Better Auth e adaptador Prisma | Alinhado; detalhes de integração não são explícitos |
| Server/Client intencional | App Router e cliente React de autenticação | Alinhado |
| Integração HTTP centralizada | `frontend/lib/auth-client.ts` | Alinhado; cookies entre origens merecem orientação específica |

## 4. Pontos de melhoria e prioridade

| ID | Prioridade | Melhoria | Evidência e limite da conclusão |
| --- | --- | --- | --- |
| B1 | Alta | Tornar a escolha de verificação dependente do escopo e ferramentas existentes | Quality gate fala em executar testes; nesta entrega o usuário os excluiu. Isso não invalida a regra geral nem justifica eliminar testes das skills |
| B2 | Alta | Detalhar integração com biblioteca de autenticação e rotas alternativas | A referência já pede proteção de caminhos alternativos, mas não oferece roteiro para endpoints nativos que modificam o mesmo usuário |
| B3 | Alta | Explicitar consistência entre sessão, atividade e revogação | Concorrência já é coberta genericamente; login simultâneo à desativação exige verificar o ciclo da biblioteca |
| B4 | Média | Mostrar como descobrir a estrutura Express e compartilhar identidade | A skill preserva a arquitetura, mas não exemplifica ordem de middleware, contexto `res.locals`/`req.user` ou separação bootstrap/app |
| B5 | Média | Orientar configuração, dependências e migrations em aplicações separadas | O projeto tem API e frontend com manifests/lockfiles distintos; a skill não detalha essa inspeção |
| B6 | Média | Esclarecer campos atribuíveis versus identidade confiável | A referência rejeita confiar em `body.role`; deve distinguir perfil do chamador de perfil atribuído a um usuário por admin autorizado |
| F1 | Média | Completar integração de sessão por cookie no frontend | A referência fala em credentials e ambiente genericamente, sem detalhar cookies, origem e SSR |
| F2 | Média | Aplicar a mesma política de verificação por escopo ao frontend | Quality gate pede testes quando fornecidos; um script instalado não prova que exista suíte nem autorização para criá-la |

## 5. Decisões que devem permanecer no projeto

Não transformar particularidades do TechPro em requisitos universais da skill:

- Perfis `ADMIN`, `PLANNING`, `TECHNICIAN` e proteção do último administrador.
- Paths `/api/users` e `/api/auth`, envelope `{ userData }` e pasta `utils/auth.ts`.
- Desativação como semântica de DELETE: seguir requisitos e documentar a decisão.
- Node.js 24, npm, PostgreSQL 17 e comandos com `--prefix api`.
- Better Auth como biblioteca obrigatória; outros projetos podem usar outra solução.
- `res.locals` como único contexto permitido; `req.user` tipado também é válido.
- Exclusão de testes na Parcial 1 como regra permanente para outros projetos.
- Uso universal de `Serializable`, SQL com lock ou criação manual de credenciais.

O snapshot de `AGENTS.md` está desatualizado: diz que há apenas `GET /health` e
nenhum modelo de negócio. Isso é um ajuste futuro deste repositório, não defeito
da skill genérica. A instrução local de testes também precisa refletir a fase de
entrega; a decisão explícita do usuário prevalece nesta sessão.

A skill recomenda diagnóstico seguro de falhas. Desativar todos os logs da
biblioteca ou imprimir apenas mensagem genérica pode reduzir observabilidade;
não modificar a skill para tornar essa escolha local uma recomendação geral.

## 6. Implementação no repositório oficial

### Etapa 1 — registrar cenários e manter o escopo

1. Localizar as duas skills no repositório oficial e ler suas instruções de contribuição.
2. Comparar com as cópias auditadas para identificar mudanças já realizadas upstream.
3. Registrar casos de uso B1–B6 e F1–F2 antes de alterar texto.
4. Preservar nomes, frontmatter, referências existentes e compatibilidade dos links.
5. Trabalhar primeiro na skill de backend; concluir sua validação antes da de frontend.

**Aceite:** a proposta diferencia orientação reutilizável de convenção local e
não pressupõe que o código atual seja o padrão obrigatório para todos os projetos.

### Etapa 2 — ajustar o entrypoint da skill de backend

Arquivo: `building-typescript-rest-apis/SKILL.md`.

- Acrescentar à inspeção inicial a descoberta do pacote que executa a API, seus
  scripts, lockfile, configuração de módulos e bootstrap.
- Distinguir implementação de API Express própria de adaptação de rotas fornecidas
  por biblioteca. Em ambos os casos, inspecionar middleware, validação e políticas.
- Adicionar uma orientação curta sobre contexto de identidade no request lifecycle,
  reaproveitando a convenção existente com tipagem adequada.
- Redigir o quality gate com condições observáveis: suíte existente, comando
  aplicável, mudança de schema e decisão explícita de escopo.
- Adicionar link para a referência Express proposta na etapa 3.

Redação sugerida, mantendo a skill em inglês:

> Determine verification from the repository's checks and the user's explicit
> scope. If an automated suite applies, run it. If the user excludes automated
> tests, run the applicable static checks and verify the affected behavior in a
> safe environment; report that no automated suite was run. A test command in a
> manifest does not establish that test files exist.

A orientação deve preservar verificações necessárias e reportar limitações.
Não remover gates existentes de CI nem adicionar infraestrutura de testes por
iniciativa da skill; mudanças nesses gates dependem do pedido e do contexto.

**Aceite:** o entrypoint continua curto e genérico, sem exigir novas pastas,
frameworks, métodos de autenticação ou criação de testes contra o escopo explícito.

### Etapa 3 — acrescentar referência prática Express

Novo arquivo: `building-typescript-rest-apis/references/express-application-structure.md`.

Conteúdo proposto:

1. Descobrir o bootstrap e a montagem do app; explicar quando separá-los se já houver necessidade.
2. Exemplo adaptável `route → middleware → controller → schema → service → persistence`.
3. Responsabilidades: caminho e método na rota; HTTP e validação no controller;
   regras/consultas no service; cliente compartilhado conforme convenção local.
4. Contexto autenticado: `res.locals` com tipo apropriado ou `req.user` com extensão
   do tipo existente. Não tratar `locals` como payload enviado automaticamente.
5. Ordem de middleware: políticas gerais, handler de biblioteca conforme seu
   contrato, parser nas rotas que o usam, rotas e tratamento global de erros.
6. Prefixos de router e endpoint de health, evitando paths duplicados.
7. Propagação de erros conforme a versão/framework; não exigir try/catch redundante
   quando o runtime já encaminha promises rejeitadas de forma adequada.

Usar um exemplo pequeno e em inglês. Não copiar os arquivos completos do TechPro.
Se a contribuição upstream exigir entrypoint menor, mover a explicação detalhada
para esta referência, mantendo apenas o link no SKILL.md.

**Aceite:** o exemplo é aplicável sem impor repositories, classes ou reestruturação.

### Etapa 4 — expandir autenticação e autorização

Arquivo: `references/authentication-and-authorization.md` da skill de backend.

Adicionar seções sobre:

- Mapeamento das rotas próprias e rotas nativas da biblioteca que alteram os mesmos
  dados: signup, profile update, email change, delete e credential changes.
- Aplicar ou restringir essas rotas conforme o produto; não bloquear todas por padrão.
- Identidade do chamador sempre vem da sessão validada. Um `role` no cadastro do
  usuário-alvo pode ser permitido quando o chamador está autorizado e o valor é validado.
- Sessões por cookie: biblioteca controla assinatura, expiração e logout; preservar
  proteções de origem/CSRF e conferir CORS com credenciais quando há origens distintas.
- Provisionamento interno: preferir APIs oficialmente suportadas pela biblioteca.
  Se o projeto já grava credenciais diretamente, verificar versão, formato, vínculo,
  hashing e atomicidade; não universalizar essa implementação.
- Desativação, alteração de perfil/email e validade da sessão segundo a regra do produto.
- Concorrência: checar atividade antes do login pode ser insuficiente se sessão for
  inserida depois da revogação. Inspecionar hooks, caches e transações antes de escolher solução.
- Rate limiter geral e específico podem coexistir; identificar escopo, unidade,
  regras especiais, `Retry-After` e armazenamento, sem desabilitar proteção para passar uma verificação.

**Aceite:** a referência ajuda a avaliar a integração existente e preserva as
políticas do produto; não exige JWT nem uma biblioteca específica.

### Etapa 5 — refinar validação, configuração e persistência

Arquivos existentes: `references/validation-and-errors.md` e
`references/prisma-and-transactions.md`.

Validação e configuração:

- Preferir tipos de entrada derivados de schema validado; tipos Prisma descrevem
  persistência, não validam o contrato HTTP.
- Explicitar writable fields, envelopes existentes e tratamento de campos extras.
- Diferenciar `.env` (valores) de módulo de configuração (carga/validação/exportação).
- Falhas de startup devem mostrar nomes de variáveis sem imprimir valores sensíveis.
- Permitir formatos nativos de erro da biblioteca quando já fazem parte do contrato;
  documentar diferenças e adaptar consumidores sem criar normalização desnecessária.

Persistência e setup:

- Conferir versão do Prisma, provider do generator, caminho gerado, adaptador e
  resolução ESM antes de copiar exemplos. Consultar documentação oficial se necessário.
- Instalar dependências no pacote consumidor e atualizar o lockfile correspondente.
- Diferenciar validar schema, gerar cliente, criar migration e aplicar migrations.
- Preservar migrations já aplicadas e avaliar SQL/data loss antes de executar.
- Distinguir nested write atômico de transação interativa para leitura seguida de
  gravação ou várias operações. Não adicionar wrapper de transação por simetria.
- Manter hashing/computação pesada fora de transações quando possível.
- Verificar tratamento de conflitos de concorrência sem impor retries automáticos.

**Aceite:** comandos e exemplos são identificados como adaptáveis à aplicação,
e saídas geradas ou dependências instaladas não são editadas manualmente.

### Etapa 6 — separar política de verificação de técnicas de teste

Arquivo: `references/api-testing.md`, com roteamento pelo SKILL.md.

1. Manter recomendações atuais de testes de comportamento, isolamento e persistência.
2. Acrescentar seção inicial para escolher a verificação aplicável ao pedido.
3. Se testes automatizados forem solicitados/aplicáveis: seguir a suíte e runner existentes.
4. Se explicitamente excluídos: conferir lint/tipos/build, migrations quando aplicáveis
   e exercitar HTTP/persistência em ambiente isolado com dados fictícios.
5. Registrar cenários, resultados e limitações sem chamar exercício manual de suíte automatizada.
6. Nunca usar dados de produção, credenciais reais ou reset/truncation sem autorização adequada.
7. Não afirmar que comandos passaram se não foram executados; reportar limitações do sandbox.

**Aceite:** testes seguem recomendados para cenários apropriados, enquanto a skill
respeita a exclusão explícita de testes e mantém verificação proporcional.

### Etapa 7 — complementar a skill de frontend

Arquivos: `developing-nextjs-app-router-interfaces/SKILL.md` e
`references/data-fetching-and-api-integration.md`.

- Manter App Router, limites Server/Client, acessibilidade, forms e estados atuais.
- Acrescentar guia curto de sessão com API separada: `credentials: include` em fetch,
  `withCredentials` em Axios e uso do cliente de autenticação já existente.
- Distinguir URL pública da API no navegador de URL interna usada no servidor/container.
- Explicar que SSR não recebe automaticamente os cookies encaminhados ao backend;
  usar o mecanismo previsto pelo projeto e não encaminhar cookies para origens arbitrárias.
- Conferir hosts/origens, cookie policy, expiração, logout, `401` e `403`.
- Evitar importar configuração de autenticação do backend no bundle do frontend.
- Derivar/validar campos adicionais da sessão quando o cliente padrão não os tipa.
- Tratar formatos de erro da API conforme contrato existente.
- Aplicar a política condicionada de verificação da etapa 6 ao gate do frontend,
  mantendo verificação de navegador para comportamentos de interface quando viável.

**Aceite:** não há imposição de nova biblioteca de fetch, estado global ou redesign;
a skill continua útil a frontends que não usam cookies ou backend separado.

## 7. Cenários de validação da skill no repositório oficial

Esta validação mede as instruções das skills; não cria uma suíte de testes do TechPro.
Usar fixtures mínimas e ambientes temporários. Ao avaliar comportamento de agente,
comparar a versão atual e a proposta com o mesmo pedido, sem antecipar a resposta
esperada no prompt do agente. Registrar decisões e artefatos efetivos.

| Cenário | Resultado esperado |
| --- | --- |
| Express com routes/controllers/services e Prisma direto | Preserva a organização e não introduz repository/classes |
| Projeto com outro arranjo funcional de pastas | Segue aquele projeto, sem impor árvore do TechPro |
| POST recebe tipo Prisma e relações arbitrárias | Define/usa contrato validado com campos permitidos |
| `res.locals.user` já existe | Reutiliza o contexto com tipo adequado, sem trocar para `req.user` por hábito |
| `req.user` tipado já existe | Reutiliza-o, sem trocar para `res.locals` por hábito |
| ADMIN cadastra usuário com campo role | Valida perfil do alvo e autoriza o chamador a atribuí-lo |
| Biblioteca de auth tem endpoint nativo de profile update | Identifica sua política e evita caminho alternativo incompatível |
| Login e desativação concorrentes | Avalia criação/revogação/caches; não se satisfaz apenas com um check inicial |
| Limites geral e específico devolvem 429 | Respeita limite/Retry-After e não desabilita proteção para verificar |
| Dependência necessária só no backend | Altera manifest/lockfile da API, sem instalar na raiz/frontend |
| Testes explicitamente fora do escopo | Executa verificações pertinentes e relata ausência de suíte automatizada |
| Projeto tem suíte automatizada e nenhum override | Roda testes relevantes e respeita gates existentes |
| Next.js com backend separado e sessão por cookie | Usa credenciais e origem corretas sem expor secrets |
| Next.js usa autenticação diferente | Preserva a integração; não força Better Auth/cookies |
| Só há schema de negócio, sem endpoints | Não declara os CRUDs implementados pela existência dos modelos |

Além dos cenários:

- Validar frontmatter e links relativos usando ferramentas disponíveis no upstream.
- Conferir que cada referência nova seja ligada pelo entrypoint.
- Revisar exemplos contra versões declaradas; não apresentar fragmentos como
  implementação completa nem acoplar a skill a versões do TechPro.
- Rever redundâncias e manter detalhes específicos nas referências apropriadas.
- Se uma mudança não melhorar decisões observáveis, removê-la em vez de acumular regras.

## 8. Sequência sugerida de commits no upstream

1. `docs(api-skill): clarify verification scope and application discovery`
2. `docs(api-skill): add adaptable Express application guidance`
3. `docs(api-skill): expand session and authentication integration guidance`
4. `docs(api-skill): refine validation and Prisma workflow references`
5. `docs(nextjs-skill): clarify cookie sessions and API integration`

Agrupar ajustes da referência de testing com o primeiro commit. Respeitar o padrão
de commits e organização do repositório oficial se diferirem desta sugestão.

## 9. Atualização das cópias neste projeto

Após aprovação e publicação das skills oficiais:

1. Importar a revisão escolhida em `.agents/skills/` pelo procedimento existente.
2. Atualizar também `.claude/skills/` ou o mecanismo de distribuição usado pela equipe.
3. Conferir igualdade das cópias e existência dos arquivos referenciados.
4. Atualizar separadamente o snapshot de implementação no `AGENTS.md`.
5. Ajustar instruções de verificação locais à fase do projeto, preservando o histórico
   da decisão sobre testes e reavaliando-o quando a fase mudar.
6. Fazer uma leitura de aplicação ao próximo CRUD, sem reimplementar usuários por
   causa da atualização da skill.

## 10. Critério final de conclusão

- A orientação geral de arquitetura existente é preservada.
- B1–B6 e F1–F2 estão endereçados com condições e exemplos reutilizáveis.
- Auth por biblioteca tem seus caminhos alternativos e ciclo de sessão avaliados.
- Verificação respeita escopo explícito, ferramentas disponíveis e gates aplicáveis.
- Nenhuma regra específica de TechPro vira obrigação universal.
- Frontmatter, referências e exemplos são verificados no upstream.
- As alterações são publicadas e depois sincronizadas nas duas cópias locais.

Este plano está pronto para ser levado ao repositório oficial. A implementação,
validação comportamental e publicação das skills ainda não foram realizadas.
