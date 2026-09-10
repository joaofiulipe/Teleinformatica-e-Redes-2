## Purpose

Define o fluxo do programa entregável da Tarefa 0 (RDT-UnB Explorer): orquestrar PING, HELLO e REQ contra o servidor RDT-UnB e imprimir a saída no formato exigido pelo enunciado.

## ADDED Requirements

### Requirement: Execução sequencial de PING, HELLO e REQ
O programa SHALL executar, nesta ordem, exatamente três etapas contra o servidor configurado: medir o RTT via PING, realizar o handshake via HELLO, e requisitar o segmento 0 via REQ.

#### Scenario: Fluxo completo bem-sucedido
- **WHEN** o programa é executado e o servidor responde a todas as três etapas dentro do timeout
- **THEN** o programa executa PING, depois HELLO, depois REQ seg=0, nessa ordem, e encerra

### Requirement: Relato do RTT medido
O programa SHALL medir o tempo decorrido entre o envio do PING e o recebimento do PONG e SHALL imprimir esse valor em milissegundos.

#### Scenario: RTT impresso após PONG
- **WHEN** o servidor responde ao PING com `PONG|time=...` antes do timeout
- **THEN** o programa imprime o RTT medido em milissegundos

### Requirement: Relato dos dados do handshake
O programa SHALL usar o identificador de grupo, tamanho de segmento e arquivo configurados para montar o HELLO, e SHALL imprimir o tamanho do arquivo, o checksum esperado, o total de segmentos e o tamanho de segmento retornados pelo servidor na resposta OK.

#### Scenario: Campos do OK impressos
- **WHEN** o servidor responde ao HELLO com `OK|file_size=...|checksum=...|seed=...|total_segments=...|segment_size=...`
- **THEN** o programa imprime o tamanho do arquivo, o checksum, o total de segmentos e o tamanho de segmento

### Requirement: Relato do segmento recebido
O programa SHALL requisitar o segmento de sequência 0 e SHALL imprimir o tamanho em bytes do payload recebido e os primeiros 8 bytes desse payload em hexadecimal.

#### Scenario: Payload do segmento 0 impresso
- **WHEN** o servidor responde ao REQ com `DATA|seq=0|total=512|<payload>`
- **THEN** o programa imprime o tamanho do payload recebido e os primeiros 8 bytes em hexadecimal, separados por espaço

### Requirement: Tratamento de ausência de resposta
O programa SHALL tratar a expiração do timeout em qualquer uma das três etapas relatando o problema de forma legível ao usuário, sem travar indefinidamente nem encerrar com uma exceção não tratada.

#### Scenario: Timeout durante qualquer etapa
- **WHEN** o servidor não responde a uma das mensagens (PING, HELLO ou REQ) dentro do timeout configurado
- **THEN** o programa informa que houve timeout naquela etapa e encerra de forma controlada, sem stack trace não tratado

### Requirement: Identificador de grupo configurável
O programa SHALL permitir configurar o identificador de grupo (por exemplo, `grupo01`) usado na mensagem HELLO sem exigir alteração do fluxo de execução, de modo que cada grupo da turma use seu próprio identificador.

#### Scenario: Execução com identificador de grupo próprio
- **WHEN** o programa é executado com o identificador de grupo do time (ex.: `grupo07`)
- **THEN** a mensagem HELLO enviada ao servidor usa exatamente esse identificador
