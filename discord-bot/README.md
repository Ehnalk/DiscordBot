# Discord Bot Project

Ein einfaches Discord Bot Projekt mit Python, inklusive WebSocket Server für Echtzeit-Kommunikation.

## Features

- **Discord Bot** mit `discord.py`
  - `!ping` - Bot-Latenz anzeigen
  - `!hello` - Bot grüßt dich
  - `!info` - Bot-Informationen
  - `!help` - Alle verfügbaren Befehle anzeigen

- **WebSocket Server**
  - Echtzeit-Verbindungen zu Clients
  - Broadcast-Nachrichten zu allen Clients
  - Status-Updates
  - Echo-Test-Funktionalität

## Project Structure

```
DiscordBot/
├── main.py                      # Discord Bot Einstiegspunkt
├── websocket_server.py          # WebSocket Server
├── .env                         # Umgebungsvariablen (Token)
├── discord-bot/
│   ├── src/
│   │   ├── main.py              # Vollständiger Discord Bot Code
│   │   ├── bot.py               # Bot Klasse
│   │   ├── cogs/                # Command-Module
│   │   │   └── __init__.py
│   │   └── utils/               # Utility-Funktionen
│   │       └── __init__.py
│   ├── tests/
│   │   └── test_basic.py        # Unit Tests
│   ├── requirements.txt         # Python Dependencies
│   ├── pyproject.toml           # Projekt-Konfiguration
│   └── README.md                # Diese Datei
├── .gitignore                   # Git ignore rules
└── Vision.txt                   # Projekt-Vision
```

## Installation

### Schritt 1: Dependencies installieren

```bash
pip install discord.py websockets python-dotenv
```

Oder mit `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Schritt 2: Discord Bot Token einrichten

1. Gehe zu [Discord Developer Portal](https://discord.com/developers/applications)
2. Erstelle eine neue Applikation
3. Erstelle einen Bot
4. Kopiere den Token
5. Fügen ihn in `.env` ein:
```
DISCORD_TOKEN = "dein_bot_token_hier"
```

⚠️ **Wichtig:** Gib deinen Token niemals öffentlich oder in Git-Repositorys preis!

## Verwendung

### Discord Bot starten

```bash
python main.py
```

Der Bot verbindet sich mit Discord und wartet auf Befehle.

### WebSocket Server starten

```bash
python websocket_server.py
```

Der Server läuft auf `ws://localhost:8765`

### Beide gleichzeitig starten (Terminal 1 & 2)

```bash
# Terminal 1: Discord Bot
python main.py

# Terminal 2: WebSocket Server
python websocket_server.py
```

## WebSocket Server API

Der WebSocket Server akzeptiert folgende JSON-Nachrichtentypen:

### Ping
```json
{
  "type": "ping"
}
```
**Antwort:** `{"type": "pong", "timestamp": "..."}`

### Broadcast
```json
{
  "type": "broadcast",
  "message": "Hallo an alle!"
}
```
Sendet Nachricht an alle verbundenen Clients.

### Status
```json
{
  "type": "status"
}
```
**Antwort:** Anzahl verbundener Clients und Server-Zeit

### Echo
```json
{
  "type": "echo",
  "data": "Hallo Echo"
}
```
**Antwort:** Echoed die gesendete Daten zurück

## Discord Bot Befehle

| Befehl | Beschreibung |
|--------|------------|
| `!help` | Zeige alle Befehle |
| `!ping` | Bot-Latenz anzeigen |
| `!hello` | Bot grüßt dich |
| `!info` | Bot- und Server-Informationen |

## Testing

Führe Tests aus mit:
```bash
python -m pytest tests/
```

## Umgebungsvariablen

Erstelle eine `.env` Datei im Root-Verzeichnis:

```
DISCORD_TOKEN = "dein_token_hier"
```

## Anforderungen

- Python 3.8+
- discord.py >= 2.0
- websockets >= 10.0
- python-dotenv >= 0.19

## Lizenz

MIT License

## Kontakt & Support

Bei Fragen oder Problemen erstelle bitte ein Issue im Repository.
