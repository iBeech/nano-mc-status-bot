# 🛰️ nano-mc-status-bot

**A lightweight Discord bot for Minecraft server hosts using custom subdomains.**  
Built for simplicity, performance, and optional Pterodactyl panel integration.

---

## ✨ Features

- `/status <subdomain>` command — e.g. `/status mc1`
- Ping any Minecraft Java Edition server using subdomains like `mc1.nanobattlestation.co.uk`
- Shows player count and latency
- **Optional:** Enhanced stats via the Pterodactyl API (RAM, state, etc.)
- Skips Pterodactyl queries if not configured
- Fully Dockerized and ready for production

---

## 🧪 Example Output

```
✅ mc1.nanobattlestation.co.uk is online with 2 player(s).
Ping: 28 ms.
Pterodactyl Info:
- Name: mc1-lobby
- RAM Limit: 4096 MB
- State: running
```

---

## 🚀 Quick Start (Docker Compose)

1. Clone this repo or create a new folder.
2. Create your `docker-compose.yml` using the example below.
3. Run the bot:

```bash
docker compose up -d
```

### 📦 `docker-compose.yml` Example

```yaml
version: "3.8"

services:
  nano-mc-status-bot:
    image: ibeech/nano-mc-status-bot:latest
    restart: unless-stopped
    environment:
      - DISCORD_BOT_TOKEN=your-discord-token
      - BASE_DOMAIN=nanobattlestation.co.uk
      - PTERO_API_URL=https://panel.example.com/api/application
      - PTERO_API_KEY=your-ptero-key (optional)
```

---

## 🔧 Environment Variables

| Variable             | Required | Description                                  |
|----------------------|----------|----------------------------------------------|
| `DISCORD_BOT_TOKEN`  | ✅       | Your Discord bot token                       |
| `BASE_DOMAIN`        | ✅       | Base domain (e.g., `nanobattlestation.co.uk`)|
| `PTERO_API_URL`      | ❌       | Pterodactyl panel API URL                    |
| `PTERO_API_KEY`      | ❌       | API key to access Pterodactyl server info    |

---

## 🐳 Docker Hub

👉 [View on Docker Hub](https://hub.docker.com/r/ibeech/nano-mc-status-bot)

---

## 🤖 Slash Command Permissions

Make sure your bot has the following permissions:
- `Read Messages`
- `Send Messages`
- `Use Application Commands`

---

## 🛠️ Roadmap

- Bedrock server support
- Uptime monitoring
- Discord rich embeds
- Web dashboard (future)

---

## 📄 License

MIT © [Tom Beech](https://github.com/iBeech)