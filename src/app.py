import os
import sys
import asyncio
from discord import Intents, Client
from dotenv import load_dotenv
from src.handlers.hltv_matches_handler import fetch_hltv_matches
from src.handlers.discord_event_handler import check_and_create_events

# Ajusta o sys.path para considerar o diretório raiz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
CRON_INTERVAL_DAYS = int(os.getenv("CRON_INTERVAL_DAYS", 2))

# Initialize Discord client
intents = Intents.default()
intents.guilds = True
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}", flush=True)

    async def scheduled_task():
        print("Running scheduled task...", flush=True)
        await fetch_hltv_matches()
        print("HLTV matches processed. Creating Discord events...", flush=True)
        await check_and_create_events(client, DISCORD_GUILD_ID, DISCORD_TOKEN)

    await scheduled_task()

    while True:
        await asyncio.sleep(CRON_INTERVAL_DAYS * 24 * 60 * 60)
        await scheduled_task()

client.run(DISCORD_TOKEN)
