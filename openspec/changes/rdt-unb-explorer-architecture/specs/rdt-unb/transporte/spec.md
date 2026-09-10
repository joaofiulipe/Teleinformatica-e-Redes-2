## Purpose

Fornece a camada de transporte UDP (socket, timeout, envio e recebimento) usada por todas as entregas do RDT-UnB, sem qualquer conhecimento do formato das mensagens trocadas com o servidor.

## ADDED Requirements

### Requirement: Criação de socket UDP com timeout configurável
O transporte SHALL criar um socket UDP (`AF_INET`/`SOCK_DGRAM`) com um timeout de recebimento configurável, aplicando um valor padrão quando nenhum for informado.

#### Scenario: Timeout padrão aplicado
- **WHEN** o transporte é iniciado sem um valor de timeout explícito
- **THEN** o socket é criado com um timeout padrão de recebimento maior que zero

#### Scenario: Timeout customizado aplicado
- **WHEN** o transporte é iniciado com um valor de timeout explícito (por exemplo, 5.0 segundos)
- **THEN** o socket é criado usando exatamente esse valor como timeout de recebimento

### Requirement: Envio de datagramas
O transporte SHALL enviar uma sequência de bytes fornecida para um endereço (host, porta) de destino, sem inspecionar ou validar o conteúdo enviado.

#### Scenario: Envio de bytes para o servidor
- **WHEN** o chamador solicita o envio de uma sequência de bytes para um endereço (host, porta)
- **THEN** o transporte envia exatamente esses bytes para esse endereço via UDP

### Requirement: Recebimento de datagramas com tratamento de timeout
O transporte SHALL aguardar um datagrama de resposta e retornar os bytes recebidos junto com o endereço de origem, e SHALL sinalizar de forma explícita quando o timeout expira sem resposta, sem travar indefinidamente.

#### Scenario: Resposta recebida dentro do timeout
- **WHEN** o servidor responde antes do timeout configurado
- **THEN** o transporte retorna os bytes recebidos e o endereço de quem respondeu

#### Scenario: Nenhuma resposta antes do timeout
- **WHEN** nenhum datagrama chega dentro do timeout configurado
- **THEN** o transporte sinaliza uma condição de timeout ao chamador em vez de bloquear indefinidamente

### Requirement: Transporte agnóstico ao protocolo de aplicação
O transporte SHALL operar apenas sobre sequências de bytes brutas, sem parsear, montar ou validar campos do protocolo RDT-UnB (PING, HELLO, REQ, DATA e similares).

#### Scenario: Reuso por múltiplas entregas
- **WHEN** uma nova entrega (Entrega 1, 2 ou 3) introduz novos tipos de mensagem ou lógica de retransmissão
- **THEN** o módulo de transporte não precisa ser alterado, pois ele não conhece o formato de nenhuma mensagem específica
