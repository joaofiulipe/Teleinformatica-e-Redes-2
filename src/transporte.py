# Exemplos do enunciado (DetalhamentoDoProjeto.md) — Dicas 1, 2 e 3.
# Apenas organizado aqui, nada foi implementado ainda.

# Dica 1 — Criar um socket UDP
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Dica 2 — Enviar e receber
servidor = ("137.131.178.229", 8080)
sock.sendto(b"PING", servidor)

dados, endereco = sock.recvfrom(65507)

# Dica 3 — Definir um timeout
sock.settimeout(5.0)  # espera no máximo 5 segundos
