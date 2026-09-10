## Purpose

Define a montagem e o parsing das mensagens do protocolo RDT-UnB (texto no formato `CAMPO=valor|CAMPO=valor` e o formato binário do pacote `DATA`), de forma independente de rede, para ser reaproveitado por todas as entregas.

## ADDED Requirements

### Requirement: Montagem da mensagem PING
O protocolo SHALL fornecer a montagem da mensagem `PING` como a sequência de bytes literal `PING`, sem parâmetros adicionais.

#### Scenario: Montar PING
- **WHEN** o chamador solicita a montagem da mensagem de ping
- **THEN** o protocolo retorna os bytes correspondentes a `PING`

### Requirement: Montagem da mensagem HELLO
O protocolo SHALL fornecer a montagem da mensagem `HELLO` a partir dos parâmetros grupo, tamanho de segmento e arquivo, no formato `HELLO|grupo=<grupo>|segment_size=<tamanho>|file=<arquivo>`.

#### Scenario: Montar HELLO com parâmetros do grupo
- **WHEN** o chamador fornece grupo=`grupo01`, segment_size=`512` e file=`small`
- **THEN** o protocolo retorna os bytes `HELLO|grupo=grupo01|segment_size=512|file=small`

### Requirement: Montagem da mensagem REQ
O protocolo SHALL fornecer a montagem da mensagem `REQ` a partir do número de sequência do segmento solicitado, no formato `REQ|seq=<n>`.

#### Scenario: Montar REQ para o segmento 0
- **WHEN** o chamador solicita o segmento de número 0
- **THEN** o protocolo retorna os bytes `REQ|seq=0`

### Requirement: Parsing genérico de campos `CHAVE=valor`
O protocolo SHALL parsear qualquer resposta textual separada por `|` em uma lista ordenada de pares chave/valor, preservando a ordem em que os campos aparecem na mensagem.

#### Scenario: Parsear resposta com múltiplos campos
- **WHEN** o protocolo recebe uma resposta textual como `OK|file_size=1048576|checksum=2c6dad...|seed=...|total_segments=2048|segment_size=512`
- **THEN** o protocolo retorna cada par chave/valor (`file_size`→`1048576`, `checksum`→`2c6dad...`, etc.) acessível individualmente

### Requirement: Parsing da resposta PONG
O protocolo SHALL extrair da resposta `PONG|time=<valor>` o valor do campo `time` retornado pelo servidor.

#### Scenario: Extrair time do PONG
- **WHEN** o protocolo recebe `PONG|time=1788377441.636`
- **THEN** o protocolo retorna o valor `1788377441.636` associado à chave `time`

### Requirement: Parsing da resposta OK do handshake
O protocolo SHALL extrair da resposta `OK|file_size=...|checksum=...|seed=...|total_segments=...|segment_size=...` cada um desses campos nomeados.

#### Scenario: Extrair campos do OK
- **WHEN** o protocolo recebe uma resposta `OK` com os campos `file_size`, `checksum`, `seed`, `total_segments` e `segment_size`
- **THEN** o protocolo retorna os cinco valores associados às suas respectivas chaves

### Requirement: Separação de cabeçalho e payload binário do DATA
O protocolo SHALL separar, na resposta `DATA|seq=<n>|total=<m>|<payload binário>`, os campos de cabeçalho (`seq`, `total`) do payload binário, delimitando o fim do cabeçalho pela posição do terceiro caractere `|` em vez de dividir a mensagem inteira por `|`, de modo que bytes `|` presentes no payload binário não corrompam o parsing.

#### Scenario: Payload sem o byte `|`
- **WHEN** o protocolo recebe `DATA|seq=0|total=512|` seguido de 512 bytes de payload que não contêm o byte `0x7C`
- **THEN** o protocolo retorna seq=0, total=512 e exatamente os 512 bytes de payload

#### Scenario: Payload contendo o byte `|`
- **WHEN** o protocolo recebe `DATA|seq=0|total=512|` seguido de um payload binário que contém um ou mais bytes iguais a `0x7C` (`|`)
- **THEN** o protocolo ainda retorna seq=0, total=512 e o payload binário completo e inalterado, sem truncá-lo no byte `|` interno
