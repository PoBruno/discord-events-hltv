
# Discord Event Bot

Este bot verifica partidas de CS2 e cria eventos no Discord com base em um arquivo JSON.

## Docker 

1. Crie um arquivo `.env` com as seguintes variáveis:
   ```
   DISCORD_TOKEN=DICORD_TOKEN
   DISCORD_GUILD_ID=DICORD_GUILD_ID
   CHANNEL_ID=CANAL_ID
   VOICE_CHANNEL_ID=VOICE_CHANNEL_ID
   CRON_INTERVAL_DAYS=1
   DESIRED_TEAMS_NAME=FURIA,paiN,Imperial,MIBR
   TIMEZONE_TZ=America/Sao_Paul
   ```

2. Execute o Docker Run:
   ```bash
   docker run --env-file .env --name discord-hltv-bot --restart on-failure -d lorthe/discord-hltv-matches:latest
   ```

## Configuração

1. Instale as dependências:
   ```bash
   python3 -m venv src/venv
   source src/venv/bin/activate
   pip install -r requirements.txt
   ```

2. Execute o bot:
   ```bash
   python3 -m src.app
   ```

# Arquitetura

```mermaid
graph TB
    User((Discord User))
    
    subgraph "Discord Bot System"
        subgraph "Discord Integration Layer"
            DiscordClient["Discord Client<br>(discord.py)"]
            EventManager["Event Manager<br>(discord.py)"]
        end
        
        subgraph "Core Application"
            MainApp["Main Application<br>(Python)"]
            Scheduler["Task Scheduler<br>(schedule)"]
            
            subgraph "Match Processing Components"
                MatchProcessor["Match Processor<br>(Python)"]
                EventCreator["Event Creator<br>(discord.py)"]
                JSONLoader["JSON Loader<br>(Python json)"]
            end
        end
        
        subgraph "Data Storage"
            MatchesJSON[("Matches Data<br>JSON File")]
            EnvConfig[("Environment Config<br>.env")]
        end
    end
    
    subgraph "External Systems"
        DiscordAPI["Discord API<br>(External Service)"]
    end

    %% Relationships
    User -->|"Interacts with"| DiscordAPI
    DiscordAPI -->|"Communicates with"| DiscordClient
    
    MainApp -->|"Initializes"| DiscordClient
    MainApp -->|"Configures"| Scheduler
    MainApp -->|"Reads"| EnvConfig
    
    Scheduler -->|"Triggers"| MatchProcessor
    MatchProcessor -->|"Reads"| MatchesJSON
    MatchProcessor -->|"Uses"| JSONLoader
    MatchProcessor -->|"Creates events via"| EventCreator
    
    EventCreator -->|"Uses"| EventManager
    EventManager -->|"Manages events through"| DiscordClient
    
    DiscordClient -->|"Creates/Updates Events"| DiscordAPI
```
