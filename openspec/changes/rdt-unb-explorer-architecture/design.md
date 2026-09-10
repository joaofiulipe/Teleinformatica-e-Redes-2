## Context

Projeto greenfield (repositório só tem `README.md` até aqui). O enunciado da Tarefa 0 (`DetalhamentoDoProjeto.md`) já avisa que as Entregas 1, 2 e 3 vão evoluir o mesmo cliente UDP para um protocolo de transferência confiável (RDT) sobre o servidor RDT-UnB — retransmissão, controle de sequência, possivelmente controle de fluxo/congestionamento. Ver `proposal.md` para a motivação de projetar a estrutura agora em vez de a cada entrega. As capabilities `rdt-unb/transporte`, `rdt-unb/protocolo` e `rdt-unb/tarefa0-explorer` definem o contrato de comportamento; este documento cobre a organização física do código e as decisões de estrutura.

## Goals / Non-Goals

**Goals:**
- Definir uma árvore de diretórios única que sirva à Tarefa 0 e seja estendida (não reescrita) pelas Entregas 1-3.
- Isolar o que é specific da Tarefa 0 (fluxo PING→HELLO→REQ e formatação de saída) do que é reutilizável por qualquer entrega (transporte e protocolo).
- Dar um lugar padronizado para as evidências exigidas pelo enunciado (capturas do Wireshark, respostas às perguntas) sem misturá-las com código.

**Non-Goals:**
- Não é objetivo desta mudança escrever qualquer código-fonte, incluindo esqueletos de funções — isso é trabalho da fase de implementação (tasks).
- Não é objetivo decidir aqui os detalhes do protocolo de confiabilidade das Entregas 1-3 (janela deslizante, timers de retransmissão, etc.); apenas garantir que a estrutura atual não impeça essas adições.
- Não cobre infraestrutura de testes automatizados de rede (fora do escopo da Tarefa 0, que depende de um servidor remoto real).

## Decisions

### 1. Três módulos de código com responsabilidades separadas

```
src/
├── transporte.py    # rdt-unb/transporte: socket UDP, timeout, envio/recebimento
├── protocolo.py      # rdt-unb/protocolo: montagem e parsing de mensagens
tarefas/
└── tarefa0.py         # rdt-unb/tarefa0-explorer: orquestra os dois módulos acima
```

**Por quê:** o enunciado já mostra o padrão que vai se repetir em toda entrega — montar uma mensagem, mandar por um socket, parsear a resposta. Se `transporte.py` não souber nada sobre o formato das mensagens (nem `PING`, nem `HELLO`, nem `DATA`), e `protocolo.py` não souber nada sobre sockets, cada entrega futura só precisa adicionar funções novas em `protocolo.py` (ex.: mensagens de ACK/NACK) e, no máximo, estender `transporte.py` com retransmissão — sem tocar no que já funciona.

**Alternativa considerada:** um único script (como o esqueleto do enunciado sugere). Rejeitada porque, embora funcione para a Tarefa 0 isolada, forçaria reescrever ou copiar/colar a lógica de socket e parsing em cada uma das próximas 3 entregas.

### 2. Um arquivo de entrypoint por entrega, não um script que cresce

`tarefas/tarefa0.py` é o único ponto que conhece a sequência específica da Tarefa 0 (PING → HELLO → REQ) e o formato de saída exato pedido no enunciado. As Entregas 1-3 ganham `tarefas/entrega1.py`, `tarefas/entrega2.py`, etc., cada um reaproveitando `src/transporte.py` e `src/protocolo.py`.

**Por quê:** cada entrega tem seu próprio formato de saída e critério de avaliação (a Tarefa 0 tem uma saída de console bem específica, ver `proposal.md`). Manter um entrypoint por entrega evita que uma mudança de comportamento de uma entrega quebre o vídeo/captura já gravado de outra, e permite rodar/gravar qualquer entrega independentemente das demais.

**Alternativa considerada:** um único `main.py` com uma flag `--entrega N`. Rejeitada por adicionar complexidade de CLI sem benefício real para um trabalho de disciplina — cada entrega é gravada e entregue separadamente.

### 3. Identificador de grupo e parâmetros de conexão como configuração, não hard-coded no meio da lógica

O nome do grupo (`grupoXX`), endereço/porta do servidor e tamanho de segmento ficam como constantes/parâmetros no topo do entrypoint (ou variáveis de ambiente), nunca embutidos dentro de `protocolo.py` ou `transporte.py`.

**Por quê:** `rdt-unb/tarefa0-explorer` exige que o identificador de grupo seja configurável sem mudar o fluxo (ver spec). Isso também facilita trocar de arquivo (`small`/`medium`/`large`) nas próximas entregas sem editar código de parsing.

### 4. Diretórios de evidência (`capturas/`, `docs/`) separados do código, um por entrega

```
capturas/
└── tarefa0/     # .pcapng do Wireshark + screenshots pedidos no enunciado
docs/
└── tarefa0-respostas.md   # respostas às perguntas da entrega
```

**Por quê:** o enunciado exige captura do Wireshark e respostas escritas como parte da entrega, mas isso não é código nem faz parte de nenhuma capability comportamental — não precisa (e não deve) virar spec. Um subdiretório por entrega evita confundir screenshots/respostas de entregas diferentes quando a Tarefa 0, 1, 2 e 3 estiverem todas no mesmo repositório.

## Risks / Trade-offs

- **[Risco]** Separar em 3 módulos desde a Tarefa 0 é mais estrutura do que o esqueleto sugerido pelo enunciado exige para uma entrega pequena. → **Mitigação:** cada módulo continua pequeno (poucas funções); o custo extra é baixo e paga-se já na Entrega 1 quando o protocolo crescer.
- **[Risco]** Se as Entregas 1-3 exigirem um modelo de concorrência diferente (ex.: sockets não-bloqueantes, threads para timers de retransmissão), o contrato atual de `rdt-unb/transporte` (chamadas síncronas simples) pode precisar de uma revisão maior, não só extensão. → **Mitigação:** tratar isso como uma nova proposta de mudança quando a Entrega 1 for especificada, em vez de tentar prever agora um contrato de concorrência sem informação suficiente.
- **[Trade-off]** Manter um entrypoint por entrega duplica algumas poucas linhas de orquestração (criar socket, chamar handshake) entre `tarefa0.py` e os futuros `entregaN.py`. Aceito porque a duplicação é pequena e o isolamento entre entregas vale mais do que o DRY nesse ponto.

## Migration Plan

Não há sistema em produção nem código existente para migrar — esta é a estrutura inicial do repositório. A "migração" relevante é para as próximas entregas:

1. Entrega 1 adiciona novas funções de mensagem em `src/protocolo.py` (ex.: mensagens de confirmação/retransmissão) e, se necessário, estende `src/transporte.py` com lógica de reenvio — sem alterar os contratos já definidos em `rdt-unb/transporte` e `rdt-unb/protocolo` para a Tarefa 0.
2. Cada nova entrega cria seu próprio `tarefas/entregaN.py`, `capturas/entregaN/` e `docs/entregaN-respostas.md`, seguindo o mesmo padrão desta mudança.
3. Caso uma entrega futura exija mudar o comportamento já especificado aqui (não apenas estendê-lo), isso deve entrar como uma nova mudança OpenSpec com uma delta `MODIFIED Requirements` sobre a capability afetada, não como edição direta do spec.
