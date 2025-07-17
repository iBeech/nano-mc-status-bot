import discord
from discord.ext import commands
from discord import app_commands
import os
import requests
from mcstatus import JavaServer

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "nanobattlestation.co.uk")
PTERO_API_KEY = os.getenv("PTERO_API_KEY")
PTERO_API_URL = os.getenv("PTERO_API_URL")

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

class StatusBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=discord.Intents.default())

    async def setup_hook(self):
        self.tree.add_command(status)
        await self.tree.sync()  # Sync commands to Discord

bot = StatusBot()

@discord.app_commands.command(name="status", description="Check the status of your Minecraft server")
@app_commands.describe(subdomain="Your subdomain, e.g. mc1")
async def status(interaction: discord.Interaction, subdomain: str):
    # Your existing status command logic, but use interaction.response.send_message(...)
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
        except Exception:
            message.append("⚠️ Failed to connect to Pterodactyl API.")

    await interaction.response.send_message("\n".join(message))

@bot.event
async def on_ready():
    print(f"Bot is live as {bot.user}")

bot.run(TOKEN)