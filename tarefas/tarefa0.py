# Estrutura sugerida do código (DetalhamentoDoProjeto.md).
# Apenas organizado aqui, nada foi implementado ainda.

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
