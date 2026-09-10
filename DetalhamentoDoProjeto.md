UDP em Ação
Disciplina: TR2 (Prof. Bordim).
Entrega: Detalhada no item "O que entregar"
Objetivo: Primeiro contato com sockets UDP em Python aplicado a um servidor real!

Ponto de partida — o que já vimos em sala
Nas últimas aulas vimos o par cliente/servidor UDP do Kurose. O cliente envia uma frase em minúsculas e o servidor devolve em maiúsculas:

Cliente UDP (Kurose):

from socket import *
serverName = 'hostname'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
Servidor UDP (Kurose):

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
Esses dois scripts mostram o essencial: como criar um socket UDP, como enviar com sendto e como receber com recvfrom. Tudo que você vai usar nesta tarefa, e nas entregas seguintes, é uma evolução desses mesmos conceitos.

Contexto desta tarefa
O servidor RDT-UnB está rodando em 137.131.178.229:8080/UDP. Assim como o servidor do Kurose, ele recebe pacotes UDP e responde. A diferença é que em vez de converter texto para maiúsculas, ele serve arquivos usando um protocolo próprio.

Nesta tarefa você vai adaptar o cliente UDP do Kurose para se comunicar com o servidor RDT-UnB. Não é necessário escrever do zero, pois o esqueleto já está pronto nas transparências e você deve evoluir a partir dele. Você vai trocar o serverName, a serverPort, e as mensagens enviadas.

A única novidade em relação ao código do Kurose é: - Definir um timeout no socket (o servidor do Kurose estava na sua máquina local, pois agora o servidor está em São Paulo e pode demorar). - Enviar mensagens no formato do protocolo RDT-UnB em vez de frases livres - Parsear a resposta que vem no formato CAMPO=valor|CAMPO=valor

O que você vai implementar
Um script Python que, ao ser executado, faz exatamente 3 coisas em sequência:

Passo 1 — Medir o RTT
Envie o pacote PING para o servidor e meça quanto tempo leva até receber o PONG de volta. Esse tempo é o RTT (Round-Trip Time) entre o seu computador e o servidor em São Paulo.

Você envia:    PING
Servidor devolve: PONG|time=1788377441.636
Imprima na tela o RTT em milissegundos. Note que o Servidor retorna junto ao PONG um valor no `time', anote esse valor, você vai precisar dele posteriormente.

Passo 2 — Fazer o handshake
Envie o pacote HELLO com os parâmetros do seu grupo e leia a resposta OK. Extraia e imprima cada campo retornado pelo servidor.

Você envia:    HELLO|grupo=grupo01|segment_size=512|file=small
Servidor devolve: OK|file_size=1048576|checksum=2c6dad...|seed=...|total_segments=2048|segment_size=512
Imprima na tela: tamanho do arquivo, checksum esperado, total de segmentos.

Passo 3 — Receber um segmento
Envie o pacote REQ para o segmento 0 e receba o DATA correspondente. Imprima o tamanho do payload recebido e os primeiros 8 bytes em hexadecimal.

Você envia:    REQ|seq=0
Servidor devolve: DATA|seq=0|total=512|<payload binário>
Saída esperada do programa
=== Tarefa 0 — RDT-UnB Explorer ===
Servidor: 137.131.178.229:8080

[1] PING
    RTT: 21.3 ms

[2] HELLO
    Arquivo:         small (1048576 bytes = 1024 KB)
    Checksum MD5:    2c6dad8d36989864d3bc093744eedf5f
    Total segmentos: 2048
    Tamanho segmento: 512 bytes

[3] REQ seg=0
    Payload recebido: 512 bytes
    Primeiros 8 bytes: a3 f1 7c 00 bb 29 e4 51
Dicas de implementação
Leia cada dica com cuidado antes de começar a escrever código.

Dica 1 — Criar um socket UDP
Um socket UDP em Python se cria com duas linhas:

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
A diferença para TCP é justamente o SOCK_DGRAM em vez de SOCK_STREAM. UDP não estabelece conexão — você simplesmente envia para um endereço e porta.

Dica 2 — Enviar e receber
Para enviar, use sendto informando o destino:

servidor = ("137.131.178.229", 8080)
sock.sendto(b"PING", servidor)
Note o b antes da string — pacotes UDP são bytes, não texto.

Para receber, use recvfrom com o tamanho máximo do buffer:

dados, endereco = sock.recvfrom(65507)
O 65507 é o tamanho máximo de um pacote UDP. Você vai receber menos que isso na prática, mas é bom ter margem.

Dica 3 — Definir um timeout
Se o servidor não responder, seu programa vai ficar esperando para sempre. Defina um timeout antes de qualquer recvfrom:

sock.settimeout(5.0)  # espera no máximo 5 segundos
Se o timeout expirar, o Python levanta uma exceção socket.timeout. Trate isso com try/except.

Dica 4 — Medir o RTT
O RTT é o tempo entre o envio e o recebimento. Use time.time() antes e depois:

import time
inicio = time.time()
sock.sendto(b"PING", servidor)
dados, _ = sock.recvfrom(65507)
rtt = (time.time() - inicio) * 1000  # converte para ms
Dica 5 — Montar o pacote HELLO
O HELLO tem campos separados por |. Monte a string e converta para bytes:

grupo = "grupo01"
pacote = f"HELLO|grupo={grupo}|segment_size=512|file=small"
sock.sendto(pacote.encode("utf-8"), servidor)
Dica 6 — Parsear a resposta do servidor
A resposta do servidor também usa | como separador. Para extrair os campos:

resposta = data.decode("utf-8")
campos = resposta.split("|")
# campos[0] = "OK"
# campos[1] = "file_size=1048576"
# campos[2] = "checksum=2c6dad..."
# ...
Para extrair o valor de um campo como file_size=1048576:

chave, valor = campos[1].split("=")
# chave = "file_size"
# valor = "1048576"
Dica 7 — Receber o segmento (DATA binário)
O pacote DATA tem um cabeçalho texto seguido de payload binário. O formato é: DATA|seq=0|total=512| + bytes do payload.

Para separar o cabeçalho do payload, encontre onde o cabeçalho termina. O cabeçalho termina após o terceiro |:

partes = dados.split(b"|")
# partes[0] = b"DATA"
# partes[1] = b"seq=0"
# partes[2] = b"total=512"
# partes[3] = primeiros bytes do payload (pode estar incompleto!)
Atenção: o payload pode conter o caractere | (é dado binário aleatório). Por isso não use split diretamente para extrair o payload — calcule o tamanho do cabeçalho e fatie:

# Cabeçalho termina após "DATA|seq=0|total=512|"
cabecalho = b"DATA|seq=0|total=512|"
payload = dados[len(cabecalho):]
Mas o seq e o total variam — como calcular o tamanho do cabeçalho? Pense: o cabeçalho tem exatamente 3 separadores |. Encontre a posição do terceiro | e fatie a partir daí.

Dica 8 — Imprimir bytes em hexadecimal
Para imprimir os primeiros 8 bytes do payload em formato hexadecimal:

primeiros = payload[:8]
hex_str = " ".join(f"{b:02x}" for b in primeiros)
print(f"Primeiros 8 bytes: {hex_str}")
Estrutura sugerida do código
Não é obrigatório seguir esta estrutura, mas ela vai ajudar a organizar:

import socket
import time

SERVIDOR = "137.131.178.229"
PORTA    = 8080
GRUPO    = "grupo01"   # substitua pelo seu grupo

def criar_socket(timeout=5.0):
    # cria e configura o socket UDP
    ...

def ping(sock, servidor):
    # envia PING, mede RTT, retorna float em ms
    ...

def hello(sock, servidor, grupo):
    # envia HELLO, parseia OK, retorna dict com os campos
    ...

def requisitar_segmento(sock, servidor, seq=0):
    # envia REQ seq=0, recebe DATA, retorna bytes do payload
    ...

def main():
    sock = criar_socket()
    servidor = (SERVIDOR, PORTA)

    print("=== Tarefa 0 — RDT-UnB Explorer ===")
    print(f"Servidor: {SERVIDOR}:{PORTA}")
    print()

    # Passo 1 — PING
    ...

    # Passo 2 — HELLO
    ...

    # Passo 3 — REQ
    ...

if __name__ == "__main__":
    main()
O que entregar
Você deverá entregar um link para um vídeo (5 min, max) ou apresentação, mostrando o programa que o seu grupo fez, com comentários explicativos do código, as capturas realizadas conforme orientações abaixo (vide Captura com Wireshark). Ao final, o grupo de responder as perguntas relacionadas.

Captura com Wireshark
Enquanto seu programa estiver rodando, capture o tráfego UDP com o Wireshark. Esta captura é obrigatória — sem ela a tarefa não está completa.

Filtro a usar no Wireshark: udp and host 137.131.178.229

O que você deve identificar e anotar na captura:

Pacote PING — identifique o pacote saindo do seu IP para 137.131.178.229:8080. Mostre o campo de dados UDP com o conteúdo PING
Pacote PONG — identifique a resposta do servidor. Mostre o IP de origem (137.131.178.229), IP de destino (seu IP) e o conteúdo PONG|time=...
Pacote HELLO — identifique o pacote com HELLO|grupo=... e mostre os campos na camada de dados
Pacote OK — identifique a resposta do servidor com OK|file_size=... e destaque os campos file_size, checksume total_segments
Pacote REQ — identifique o REQ|seq=0 enviado pelo seu cliente
Pacote DATA — identifique a resposta com DATA|seq=0|total=512| e observe que o payload aparece como dados binários
Screenshots obrigatórios:

Screenshot 1: visão geral da captura mostrando a sequência de pacotes (PING → PONG → HELLO → OK → REQ → DATA) com IPs de origem e destino visíveis
Screenshot 2: detalhe do pacote OK com os campos expandidos nas camadas Ethernet, IP, UDP e dados
Screenshot 3: detalhe do pacote DATA mostrando o cabeçalho texto e o payload binário
A captura deve mostrar claramente o IP do servidor (137.131.178.229) e o seu IP local. Isso confirma que o programa realmente se comunicou com o servidor — não é possível fabricar essa evidência.

Por que isso importa antes das entregas: Nas Entregas 1, 2 e 3 você vai precisar usar o Wireshark para identificar retransmissões e medir RTT. A Tarefa 0 é o momento de aprender a ferramenta sem pressão de nota.

Perguntas
Antes da próxima aula, tente responder:

O RTT que você mediu foi sempre o mesmo em execuções diferentes? Por quê?
O `time' que retorna do servidor, o que ele de fato representa? Ele poderia ser utilizado para estimar o RTT?
O que acontece se você executar o programa duas vezes seguidas com o mesmo grupo? O checksum muda?
Se você pedir o segmento 0 duas vezes, os bytes recebidos são iguais? O que isso diz sobre o servidor?
O UDP garante que o pacote vai chegar? O que aconteceria se você não colocasse o timeout?
Por que o cabeçalho do DATA termina com | e não podemos usar split("|") diretamente para extrair o payload?
Informações do servidor
Parâmetro	Valor
Endereço	137.131.178.229
Porta	8080/UDP
Arquivos	small (1MB) · medium (5MB) · large (10MB)
Argumento grupo	Use exatamente grupo01, grupo02, etc. conforme sua turma
