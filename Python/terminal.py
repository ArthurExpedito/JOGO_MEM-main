import asyncio
import websockets
import sys

async def terminal_client(ip, port):
    uri = f"ws://{ip}:{port}"
    async with websockets.connect(uri) as websocket:
        print(f"[Conectado] {uri}")
        print("Digite comandos (ex: CONNECT, TURN 1 2, END)")

        async def receber():
            try:
                async for msg in websocket:
                    print(f"\n[Servidor] {msg}")
            except websockets.ConnectionClosed:
                print("Conexão encerrada.")

        async def enviar():
            while True:
                msg = input(">>> ").strip()
                if msg.upper() == "END":
                    await websocket.send("END")
                    await websocket.close()
                    break
                else:
                    await websocket.send(msg)

        await asyncio.gather(receber(), enviar())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python terminal.py <IP> <PORTA>")
        sys.exit(1)
    asyncio.run(terminal_client(sys.argv[1], sys.argv[2]))