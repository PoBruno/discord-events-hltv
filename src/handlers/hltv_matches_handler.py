
import json
import pytz
import random
import asyncio
import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup
from src.utils.timezone import get_timezone

#timezone_tz = pytz.timezone("America/Sao_Paulo")
timezone_tz = get_timezone()

async def fetch_hltv_matches():
    scraper = cloudscraper.create_scraper()
    url = 'https://www.hltv.org/matches'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    for _ in range(10):
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            break
        await asyncio.sleep(random.uniform(1, 3))

    soup = BeautifulSoup(response.text, 'html.parser')
    match_containers = soup.find_all('div', class_='upcomingMatch')
    matches = []

    for match in match_containers:
        teams = match.find_all('div', class_='matchTeamName text-ellipsis')
        datetime_element = match.find('div', class_='matchTime')
        event = match.find('div', class_='matchEventName gtSmartphone-only')

        if teams and datetime_element and event and datetime_element.has_attr('data-unix'):
            match_info = {
                'team1': teams[0].text.strip() if len(teams) > 0 else None,
                'team2': teams[1].text.strip() if len(teams) > 1 else None,
                'datetime': int(datetime_element['data-unix']),
                'event': event.text.strip()
            }
            matches.append(match_info)

    if matches:
        df_matches = pd.DataFrame(matches)
        if 'datetime' in df_matches.columns:
            df_matches['datetime'] = pd.to_datetime(df_matches['datetime'], unit='ms')
            df_matches['datetime'] = df_matches['datetime'].dt.tz_localize('UTC').dt.tz_convert(timezone_tz)
            df_matches['datetime'] = df_matches['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

            for match, formatted_datetime in zip(matches, df_matches['datetime']):
                match['datetime'] = formatted_datetime

            output_file = "./src/data/hltv_matches.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(matches, f, ensure_ascii=False, indent=4)
            print(f"Arquivo exportado com sucesso: {output_file}", flush=True)
        else:
            print("Nenhum dado de datetime válido encontrado.", flush=True)
    else:
        print("Nenhum match encontrado.")
        
