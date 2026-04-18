import asyncio
import websockets
import json
import logging
from datetime import datetime
from typing import Set

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Speichert alle verbundenen WebSocket-Clients
connected_clients: Set[websockets.WebSocketServerProtocol] = set()


async def handle_client(websocket, path):
    """Behandelt neue WebSocket-Verbindungen."""
    client_ip = websocket.remote_address[0]
    logger.info(f"✅ Client verbunden: {client_ip}")
    connected_clients.add(websocket)

    try:
        # Begrüßungsnachricht
        welcome_message = {
            "type": "connection",
            "status": "connected",
            "message": "Willkommen beim Discord Bot WebSocket Server!",
            "timestamp": datetime.now().isoformat(),
            "clients_connected": len(connected_clients)
        }
        await websocket.send(json.dumps(welcome_message))

        # Nachrichten von Client empfangen
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"📨 Nachricht von {client_ip}: {data}")

                # Verarbeite verschiedene Nachrichtentypen
                if data.get("type") == "ping":
                    response = {
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(response))

                elif data.get("type") == "broadcast":
                    # Sende an alle verbundenen Clients
                    broadcast_msg = {
                        "type": "broadcast",
                        "from": client_ip,
                        "message": data.get("message"),
                        "timestamp": datetime.now().isoformat()
                    }
                    await broadcast(json.dumps(broadcast_msg), exclude=websocket)

                elif data.get("type") == "status":
                    # Sende Status-Information
                    status = {
                        "type": "status",
                        "clients_connected": len(connected_clients),
                        "server_time": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(status))

                elif data.get("type") == "echo":
                    # Echo-Test
                    echo_response = {
                        "type": "echo",
                        "data": data.get("data"),
                        "received_at": datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(echo_response))

                else:
                    error = {
                        "type": "error",
                        "message": "Unbekannter Nachrichtentyp",
                        "received": data.get("type")
                    }
                    await websocket.send(json.dumps(error))

            except json.JSONDecodeError:
                error = {
                    "type": "error",
                    "message": "Ungültiges JSON-Format"
                }
                await websocket.send(json.dumps(error))

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"❌ Client getrennt: {client_ip}")
    finally:
        connected_clients.discard(websocket)


async def broadcast(message: str, exclude=None):
    """Sendet eine Nachricht an alle verbundenen Clients."""
    if not connected_clients:
        return

    disconnected = set()

    for client in connected_clients:
        if exclude and client == exclude:
            continue

        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            disconnected.add(client)

    # Entferne getrennte Clients
    connected_clients.difference_update(disconnected)


async def main():
    """Startet den WebSocket Server."""
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    logger.info("🚀 WebSocket Server läuft auf ws://0.0.0.0:8765")
    logger.info("   Lokal: ws://localhost:8765")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
