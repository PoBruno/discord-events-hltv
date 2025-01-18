
# Discord Event Bot

Este bot verifica partidas de CS2 e cria eventos no Discord com base em um arquivo JSON.

## Configuração

1. Crie um arquivo `.env` com as seguintes variáveis:
   ```
   DISCORD_TOKEN=DICORD_TOKEN
   DISCORD_GUILD_ID=DICORD_GUILD_ID
   CHANNEL_ID=CANAL_ID
   VOICE_CHANNEL_ID=VOICE_CHANNEL_ID
   CRON_INTERVAL_DAYS=3
   DESIRED_TEAMS_NAME=FURIA,paiN,Imperial,MIBR
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o bot:
   ```bash
   python app.py
   ```
```
