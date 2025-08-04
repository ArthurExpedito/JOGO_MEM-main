import asyncio
import websockets
import random
import sys

ROWS, COLS = 4, 4

# Tabuleiro
def gerar_tabuleiro():
    naipes = ['c', 's', 'h', 'd']
    valores = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10','J','Q','K']
    cartas = [f"{v}{n}" for v in valores for n in naipes][:ROWS * COLS // 2]
    baralho = cartas * 2
    random.shuffle(baralho)
    return [baralho[i * COLS:(i + 1) * COLS] for i in range(ROWS)]

# Estado do jogo
tabuleiro = gerar_tabuleiro()
visivel = [['##' for _ in range(COLS)] for _ in range(ROWS)]
pontuacao = [0, 0]  # [cliente, servidor]
vez_cliente = True
jogadas = []

# V para cartas viradas e X para não viradas
def formatar_estado_tabuleiro():
    estado = []
    for linha in visivel:
        estado.append('\t'.join(['v' if carta != '##' else 'x' for carta in linha]))
    return "BOARD\n" + '\n'.join(estado)

# Verifica se o jogo terminou
def fim_de_jogo():
    return all(carta != '##' for linha in visivel for carta in linha)

# Processa a jogada do cliente
async def processar_turno(ws, row, col):
    global vez_cliente, jogadas, pontuacao, visivel

    if not (0 <= row < ROWS and 0 <= col < COLS):
        await ws.send("ERRO posição inválida")
        return

    if visivel[row][col] != '##':
        await ws.send("ERRO posição inválida")
        return

    valor = tabuleiro[row][col]
    visivel[row][col] = valor
    jogadas.append((row, col, valor))

    await ws.send(f"CARD {row} {col} {valor}")
    await ws.send(formatar_estado_tabuleiro())

    if len(jogadas) == 2:
        await asyncio.sleep(1)
        (r1, c1, v1), (r2, c2, v2) = jogadas

        if v1 == v2:
            await ws.send("MATCH")
            pontuacao[0] += 1
        else:
            await ws.send("NO_MATCH")
            visivel[r1][c1] = '##'
            visivel[r2][c2] = '##'
            vez_cliente = False

        await ws.send(f"SCORE {pontuacao[0]} {pontuacao[1]}")
        await ws.send(formatar_estado_tabuleiro())
        jogadas.clear()

        if fim_de_jogo():
            if pontuacao[0] > pontuacao[1]:
                await ws.send("WINNER 1")
            elif pontuacao[1] > pontuacao[0]:
                await ws.send("WINNER 2")
            else:
                await ws.send("WINNER DRAW")
            await ws.send("END")
        else:
            if vez_cliente:
                await ws.send("YOUR_TURN")
            else:
                await ws.send("WAIT")
                await asyncio.sleep(2)
                await jogada_servidor(ws)

# Jogada servidor
async def jogada_servidor(ws):
    global vez_cliente, jogadas, pontuacao
    posicoes = [(r, c) for r in range(ROWS) for c in range(COLS) if visivel[r][c] == '##']
    random.shuffle(posicoes)
    (r1, c1), (r2, c2) = posicoes[:2]

    for r, c in [(r1, c1), (r2, c2)]:
        valor = tabuleiro[r][c]
        visivel[r][c] = valor
        await ws.send(f"CARD {r} {c} {valor}")
        jogadas.append((r, c, valor))
        await asyncio.sleep(1)
        await ws.send(formatar_estado_tabuleiro())

    (r1, c1, v1), (r2, c2, v2) = jogadas

    if v1 == v2:
        await ws.send("MATCH")
        pontuacao[1] += 1
    else:
        await ws.send("NO_MATCH")
        visivel[r1][c1] = '##'
        visivel[r2][c2] = '##'
        vez_cliente = True

    await ws.send(f"SCORE {pontuacao[0]} {pontuacao[1]}")
    await ws.send(formatar_estado_tabuleiro())
    jogadas.clear()

    if fim_de_jogo():
        if pontuacao[0] > pontuacao[1]:
            await ws.send("WINNER 1")
        elif pontuacao[1] > pontuacao[0]:
            await ws.send("WINNER 2")
        else:
            await ws.send("WINNER DRAW")
        await ws.send("END")
    else:
        if vez_cliente:
            await ws.send("YOUR_TURN")
        else:
            await ws.send("WAIT")
            await asyncio.sleep(2)
            await jogada_servidor(ws)

# Trata mensagens recebidas
async def tratar_mensagem(ws, msg):
    partes = msg.strip().split()
    if not partes:
        return

    comando = partes[0].upper()

    if comando == "CONNECT":
        await ws.send("WELCOME")
        await ws.send("START")
        await ws.send(formatar_estado_tabuleiro())
        await ws.send("YOUR_TURN")

    elif comando == "TURN":
        if len(partes) != 3 or not partes[1].isdigit() or not partes[2].isdigit():
            await ws.send("ERRO comando inválido")
            return
        if not vez_cliente:
            await ws.send("WAIT")
            return
        row, col = int(partes[1]), int(partes[2])
        await processar_turno(ws, row, col)

    elif comando == "END":
        await ws.send("END")
        await ws.close()

    else:
        await ws.send("ERRO comando inválido")

# Gerencia cliente
async def handler(ws, path):
    try:
        async for msg in ws:
            await tratar_mensagem(ws, msg)
    except websockets.ConnectionClosed:
        print("Cliente desconectado.")

# Execução principal com IP e porta por terminal
async def main():
    if len(sys.argv) != 3:
        print("Uso: python server.py <IP> <PORTA>")
        return
    ip = sys.argv[1]
    port = int(sys.argv[2])
    async with websockets.serve(handler, ip, port):
        print(f"Servidor rodando em ws://{ip}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())