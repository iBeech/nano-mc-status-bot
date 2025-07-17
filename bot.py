# nano-mc-status-bot: Discord bot to fetch live Minecraft server status via subdomain

"""
nano-mc-status-bot is a lightweight, Docker-friendly Discord bot that allows users to check the real-time status of their Minecraft Java servers using custom subdomains (e.g., mc1.nanobattlestation.co.uk).

Features:
- Simple `/status <subdomain>` command
- Fast ping + player count reporting
- Optional Pterodactyl API integration for detailed server info (RAM, state, etc.)
- Skips Pterodactyl queries if no API key is provided
- Easily configurable via environment variables for Docker/Compose setups
"""

import discord
from discord.ext import commands
from mcstatus import JavaServer
import requests
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "nanobattlestation.co.uk")
PTERO_API_URL = os.getenv("PTERO_API_URL")  # e.g., https://panel.example.com/api/application
PTERO_API_KEY = os.getenv("PTERO_API_KEY")  # Optional, if Pterodactyl integration is desired

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.command(name="status")
async def status(ctx, subdomain: str):
    fqdn = f"{subdomain}.{BASE_DOMAIN}"
    message = []

    try:
        server = JavaServer.lookup(fqdn)
        status = server.status()
        message.append(f"**{fqdn}** is online with **{status.players.online}** player(s).\nPing: `{round(status.latency)} ms`.")
    except Exception:
        message.append(f"❌ Could not fetch Minecraft ping status for `{fqdn}`.")

    if PTERO_API_KEY and PTERO_API_URL:
        try:
            headers = {"Authorization": f"Bearer {PTERO_API_KEY}", "Accept": "Application/vnd.pterodactyl.v1+json"}
            response = requests.get(f"{PTERO_API_URL}/servers", headers=headers)
            if response.ok:
                servers = response.json().get("data", [])
                for s in servers:
                    if subdomain.lower() in s["attributes"]["name"].lower():
                        info = s["attributes"]
                        message.append(f"Pterodactyl Info:\n- Name: `{info['name']}`\n- RAM Limit: `{info['limits']['memory']} MB`\n- State: `{info['status']}`")
                        break
            else:
                message.append("⚠️ Pterodactyl API error: could not fetch server data.")
        except Exception as e:
            message.append("⚠️ Failed to connect to Pterodactyl API.")

    await ctx.send("\n".join(message))

@bot.event
async def on_ready():
    print(f"Bot is live as {bot.user}")

bot.run(TOKEN)
