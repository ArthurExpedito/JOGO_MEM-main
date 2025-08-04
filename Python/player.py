import websockets
import asyncio

flag = False
# Recebe mensagens do servidor
async def receber_msg(websocket):
    try:
        async for msg in websocket:
            server_message = msg
            print(f"\n[Servidor] {msg}")
            await verify_turn(server_message)
    except websockets.ConnectionClosed:
        print("Conexão encerrada pelo servidor.")
        

# Envia um comando TURN após validação
async def turn_card(websocket, msg):
    if flag==True:
        mainstring = msg.upper().split()
        if len(mainstring) == 3 and mainstring[0] == "TURN":
            if mainstring[1].isdigit() and mainstring[2].isdigit():
                await websocket.send(msg)
            else:
                print("Os argumentos após TURN devem ser números.")
        else:
            print("Formato inválido. Use: TURN row col")
    else: print("ne sua ves nao parsa, fica qietin ai")

# Encerra a conexão
async def end(websocket):
    print("Encerrando a conexão com o servidor.")
    try:
        await websocket.close()
        print ("Conexão fechada")
    except Exception as e:
        print(f"Erro ao fechar a conexão: {e}")
        print("tentando novamente.")
        await end(websocket)

# Lê comandos do usuário e os envia para o servidor
async def input_read(websocket):
    print("Comandos disponíveis: TURN row col, END")
    while True:
        comando = input("Insira o comando: ").strip()
        if comando.upper() == "END":
            await end(websocket)
            break
        else:
            await turn_card(websocket, comando)

async def verify_turn(msg):
    global flag
    command = msg.split()
    flag = (command[0] == "True")
        

# Função principal que conecta e gerencia tudo
async def connect():
    uri = "ws://192.168.2.111:8765"  # Substitua pelo IP correto
    async with websockets.connect(uri) as websocket:
        print("Conectado ao servidor.")
        
        # Envia o comando CONNECT ao iniciar
        await websocket.send("CONNECT")
        
        # Cria as tarefas de receber e enviar mensagens
        receber = asyncio.create_task(receber_msg(websocket))
        enviar = asyncio.create_task(input_read(websocket))
        await asyncio.gather(receber, enviar)

# Ponto de entrada do programa
async def main():
    await connect()

# Executa o programa
asyncio.run(main())
