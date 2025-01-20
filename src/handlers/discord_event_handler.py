import os
import json
import aiohttp
from datetime import datetime, timedelta
from src.utils.timezone import get_timezone

class DiscordEvents:
    def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization': f'Bot {discord_token}',
            'User-Agent': 'DiscordBot (https://your.bot/url, Python/3.9 aiohttp/3.8.1)',
            'Content-Type': 'application/json'
        }

    async def list_guild_events(self, guild_id: int) -> list:
        url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def create_guild_event(self, guild_id: int, event_name: str, event_description: str, event_start_time: str, event_end_time: str, channel_id: int) -> None:
        url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        data = {
            'name': event_name,
            'privacy_level': 2,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'description': event_description,
            'channel_id': channel_id,
            'entity_type': 2
        }

        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            async with session.post(url, json=data) as response:
                response.raise_for_status()
                print(f'Event created: {event_name}')

async def check_and_create_events(client, guild_id, discord_token):
    events_api = DiscordEvents(discord_token)
    existing_events = await events_api.list_guild_events(guild_id)
    existing_event_names = {event['name'] for event in existing_events}

    with open('src/data/hltv_matches.json', 'r') as file:
        matches = json.load(file)

    desired_teams = os.getenv('DESIRED_TEAMS_NAME', '').split(',')
    tz = get_timezone()

    for match in matches:
        if match['team1'] in desired_teams or match['team2'] in desired_teams:
            event_name = f"{match['team1']} vs {match['team2']}"
            event_time = tz.localize(datetime.strptime(match['datetime'], '%Y-%m-%d %H:%M:%S'))
            if event_name not in existing_event_names:
                event_description = f"**Match:** {match['team1']} vs {match['team2']} - {match['datetime'], '%Y-%m-%d %H:%M:%S'} \n**Event:** {match['event']}"
                await events_api.create_guild_event(
                    guild_id=guild_id,
                    event_name=event_name,
                    event_description=event_description,
                    event_start_time=event_time.isoformat(),
                    event_end_time=(event_time + timedelta(hours=2)).isoformat(),
                    channel_id=int(os.getenv('VOICE_CHANNEL_ID'))
                )
