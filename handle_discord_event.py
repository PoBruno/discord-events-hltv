import json
import aiohttp
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
VOICE_CHANNEL_ID = int(os.getenv('VOICE_CHANNEL_ID'))
DESIRED_TEAMS_NAME = os.getenv('DESIRED_TEAMS', '')

class DiscordEvents:
    def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization': f'Bot {discord_token}',
            'User-Agent': 'DiscordBot (https://your.bot/url, Python/3.9 aiohttp/3.8.1)',
            'Content-Type': 'application/json'
        }

    async def list_guild_events(self, guild_id: int) -> list:
        event_retrieve_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.get(event_retrieve_url) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                print(f'EXCEPTION: {e}')
                return []

    async def create_guild_event(self, guild_id: int, event_name: str, event_description: str, event_start_time: str, event_end_time: str, channel_id: int, event_privacy_level=2) -> None:
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        event_data = json.dumps({
            'name': event_name,
            'privacy_level': event_privacy_level,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'description': event_description,
            'channel_id': channel_id,
            'entity_type': 2  # Event type for voice events
        })

        print(f"Sending data: {event_data}")

        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    response.raise_for_status()
                    print(f'Evento criado: {event_name}')
            except Exception as e:  
                print(f'EXCEPTION: {e}')

async def check_and_create_events(client, guild_id, discord_token):
    events_api = DiscordEvents(discord_token)  
    existing_events = await events_api.list_guild_events(guild_id)
    existing_event_names = {event['name'] for event in existing_events}

    with open('hltv_matches.json', 'r') as file:
        matches = json.load(file)

    # Lista de equipes desejadas
    #desired_teams = ['FURIA', 'paiN', 'Imperial']
    desired_teams = [team.strip() for team in DESIRED_TEAMS_NAME.split(',') if team.strip()]

    filtered_matches = [match for match in matches if match['team1'] in desired_teams or match['team2'] in desired_teams]

    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')

    def convert_to_local_time(time_str):
        naive_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        local_time = sao_paulo_tz.localize(naive_time)
        return local_time

    for match in filtered_matches:
        event_name = f"{match['team1']} vs {match['team2']}"
        event_time = convert_to_local_time(match['datetime'])
        event_start_time = event_time.isoformat()
        event_end_time = (event_time + timedelta(hours=2)).isoformat()  # Assuming the event lasts for 2 hours

        if event_name not in existing_event_names:
            event_description = f"- **Partida:** `{match['team1']}` vs `{match['team2']}`\n- **Evento:** __{match['event']}__"
            await events_api.create_guild_event(
                guild_id=guild_id,
                event_name=event_name,
                event_description=event_description,
                event_start_time=event_start_time,
                event_end_time=event_end_time,
                channel_id=VOICE_CHANNEL_ID,
                event_privacy_level=2
            )
