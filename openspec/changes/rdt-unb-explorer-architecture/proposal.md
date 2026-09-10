## Why

A Tarefa 0 da disciplina TR2 pede um cliente UDP em Python que converse com o servidor RDT-UnB (PING/PONG, HELLO/OK, REQ/DATA). O enunciado já avisa que as Entregas 1, 2 e 3 vão evoluir esse mesmo cliente para um protocolo de transferência confiável (retransmissão, controle de sequência, etc.) sobre o mesmo servidor. Se o código da Tarefa 0 for escrito como um único script solto, cada entrega futura vai reescrever ou duplicar a mesma lógica de socket e de parsing de mensagens. Definir agora uma arquitetura modular evita retrabalho e dá um lugar natural para crescer a confiabilidade nas próximas entregas.

## What Changes

- Definir a estrutura de diretórios do projeto separando três responsabilidades: transporte UDP (socket + timeout), protocolo RDT-UnB (montagem/parsing de mensagens `CAMPO=valor|...` e do formato binário do `DATA`), e o entrypoint específico de cada tarefa/entrega.
- Especificar o contrato do módulo de transporte: criação de socket UDP, configuração de timeout, envio e recebimento, sem qualquer conhecimento do formato das mensagens do servidor.
- Especificar o contrato do módulo de protocolo: funções puras para montar `PING`, `HELLO|...`, `REQ|seq=N` e para parsear `PONG|...`, `OK|...` e o cabeçalho + payload binário de `DATA|...`, sem abrir nem usar sockets.
- Especificar o comportamento do entrypoint da Tarefa 0 (`tarefa0.py`): orquestra transporte + protocolo para executar PING → HELLO → REQ(seg=0) em sequência e imprimir a saída no formato pedido pelo enunciado.
- Reservar diretórios de apoio (fora do código) para as capturas do Wireshark e para as respostas às perguntas de cada entrega, um por entrega, já antecipando Entregas 1-3.
- Nenhum código é escrito nesta mudança — esta proposta cobre apenas a arquitetura/estrutura a ser seguida quando a implementação começar.

## Capabilities

### New Capabilities
- `rdt-unb/transporte`: wrapper de socket UDP (criação, timeout, envio, recebimento) reutilizável por todas as entregas.
- `rdt-unb/protocolo`: montagem e parsing das mensagens do protocolo RDT-UnB (texto `CAMPO=valor|...` e o formato binário do `DATA`), independente de rede.
- `rdt-unb/tarefa0-explorer`: fluxo do entrypoint da Tarefa 0 (RDT-UnB Explorer) que orquestra PING, HELLO e REQ e imprime a saída esperada.

### Modified Capabilities
(nenhuma — projeto greenfield, não há specs existentes)

## Impact

- Cria a árvore de diretórios do projeto (`src/`, `tarefas/`, `capturas/`, `docs/`) que passa a ser a organização padrão para esta e as próximas entregas.
- Não afeta nenhum código existente (repositório ainda não tem implementação).
- Estabelece o contrato que as Entregas 1-3 vão estender (ex.: `rdt-unb/protocolo` ganhará mensagens novas, `rdt-unb/transporte` poderá ganhar retransmissão) sem quebrar o que for construído para a Tarefa 0.
