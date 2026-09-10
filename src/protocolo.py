# Exemplos do enunciado (DetalhamentoDoProjeto.md) — Dicas 5, 6, 7 e 8.
# Apenas organizado aqui, nada foi implementado ainda.

# Dica 5 — Montar o pacote HELLO
grupo = "grupo01"
pacote = f"HELLO|grupo={grupo}|segment_size=512|file=small"
sock.sendto(pacote.encode("utf-8"), servidor)

# Dica 6 — Parsear a resposta do servidor
resposta = data.decode("utf-8")
campos = resposta.split("|")
# campos[0] = "OK"
# campos[1] = "file_size=1048576"
# campos[2] = "checksum=2c6dad..."
# ...

chave, valor = campos[1].split("=")
# chave = "file_size"
# valor = "1048576"

# Dica 7 — Receber o segmento (DATA binário)
partes = dados.split(b"|")
# partes[0] = b"DATA"
# partes[1] = b"seq=0"
# partes[2] = b"total=512"
# partes[3] = primeiros bytes do payload (pode estar incompleto!)

# Cabeçalho termina após "DATA|seq=0|total=512|"
cabecalho = b"DATA|seq=0|total=512|"
payload = dados[len(cabecalho):]

# Dica 8 — Imprimir bytes em hexadecimal
primeiros = payload[:8]
hex_str = " ".join(f"{b:02x}" for b in primeiros)
print(f"Primeiros 8 bytes: {hex_str}")
