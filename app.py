import os  
import asyncio  
import discord  
from dotenv import load_dotenv  
from handle_hltv_matches import hltv_matches  
from handle_discord_event import check_and_create_events  

# Carregar variáveis de ambiente
load_dotenv()  
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))  
CRON_INTERVAL_DAYS = int(os.getenv('CRON_INTERVAL_DAYS', 3))  

# Inicializar cliente do Discord
intents = discord.Intents.default()  
intents.guilds = True  
client = discord.Client(intents=intents)  

@client.event  
async def on_ready():  
    print(f"Bot conectado como {client.user}")  

    async def scheduled_task():  
        print("Executando tarefa agendada...")  
        await hltv_matches()  # Primeiro, execute handle_matches para gerar o JSON novo  
        print("Matches processados. Iniciando verificação e criação de eventos...")  
        await check_and_create_events(client, DISCORD_GUILD_ID, DISCORD_TOKEN)  # Em seguida, execute check_and_create_events  

    # Executar imediatamente no início  
    await scheduled_task()  

    # Agendar a tarefa periódica  
    while True:  
        await asyncio.sleep(CRON_INTERVAL_DAYS * 24 * 60 * 60)  # Intervalo em dias  
        await scheduled_task()  

# Iniciar o bot  
client.run(DISCORD_TOKEN)  